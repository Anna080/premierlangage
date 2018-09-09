# coding: utf-8

import time

import htmlprint
from enumfields import EnumIntegerField
from jsonfield import JSONField
from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.template import Template, RequestContext
from django.template.loader import get_template

from lti.models import LTIModel, LTIgrade
from loader.models import PLTP, PL
from playexo.enums import State, EnvStatus
from playexo.request import SandboxBuild, SandboxEval



class Activity(LTIModel, LTIgrade):
    name = models.CharField(max_length=200, null=False)
    open = models.BooleanField(null=False, default=True)
    pltp = models.ForeignKey(PLTP, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + " " + self.name



class SessionActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    current_pl = models.ForeignKey(PL, on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = ('user', 'activity')
    
    
    def exercise(self, pl=None):
        """Return the SessionExercice corresponding to self.current_pl.
        
        If the optionnal parameter 'pl' is given, will instead return the SessionExercice
        corresponding to pl.
        
        Raise IntegrityError if no session for either self.current_pl or pl was found."""
        try:
            return next(i for i in self.sessionexercise_set.all() if i.pl == (self.current_pl if not pl else pl))
        except StopIteration:
            raise IntegrityError("'current_pl' of SessionActivity does not have a corresponding "
                                 + "SessionExercise")



class SessionExercise(models.Model):
    pl = models.ForeignKey(PL, on_delete=models.CASCADE, null=True)
    activity_session = models.ForeignKey(SessionActivity, on_delete=models.CASCADE)
    built = models.BooleanField(default=False)
    envid = models.UUIDField(null=True)
    context = JSONField(null=True)
    
    class Meta:
        unique_together = ('pl', 'activity_session')
    
    
    @receiver(post_save, sender=SessionActivity)
    def create_session_exercise(sender, instance, created, **kwargs):
        if created:
            for pl in instance.activity.pltp.pl.all():
                SessionExercise.objects.create(activity_session=instance, pl=pl)
            SessionExercise.objects.create(activity_session=instance)  # For the pltp
    
    
    def save(self, *args, **kwargs):
        if not self.context:
            if self.pl:
                self.context = dict(self.pl.json)
            else:
                self.context = dict(self.activity_session.activity.pltp.json)
            self.context['activity_id__'] = self.activity_session.activity.id
        super().save(*args, **kwargs)
    
    
    def add_to_context(self, key, value):
        self.context[key] = value
        self.save()
    
    
    def evaluate(self, uuid, answers):
        context = {}
        evaluator = SandboxEval(uuid, answers)
        if not evaluator.check():
            self.build()
            evaluator = SandboxEval(self.context['id__'], answers)
        
        response = evaluator.call()
        answer = {
            "answers": answers,
            "user": self.activity_session.user,
            "pl": self.pl,
            "activity": self.activity_session.activity,
        }
        
        if response['status'] < 0: # Sandbox Error
            feedback = response['feedback']
            if self.activity_session.user.profile.can_load() and response['sandboxerr']:
                feedback += "<br><br>" + htmlprint.code(response['sandboxerr'])
        
        elif response['status'] > 0:  # Evaluator Error
            feedback = ("Une erreur s'est produite lors de l'exécution du script d'évaluation "
                        + ("(exit code: %d, env: %s). Merci de prévenir votre professeur"
                           % (response['status'], response['id'])))
            if self.activity_session.user.profile.can_load():
                feedback += "<br><br>Received on stderr:<br>" + htmlprint.code(response['stderr'])
        
        else: # Success
            context = dict(response['context'])
            feedback = response['feedback']
            if self.activity_session.user.profile.can_load() and response['stderr']:
                feedback += "<br><br>Received on stderr:<br>" + htmlprint.code(response['stderr'])
            answer["grade"] = response['grade']
            answer["seed"] = context['seed'],
        
        keys = list(response.keys())
        for key in keys:
            response[key+"__"] = response[key]
        for key in keys:
            del response[key]
        del response['context__']
        context.update(response)
        
        dic = dict(self.context)
        dic.update(context)
        
        return answer, feedback, dic
    
    
    def build(self):
        response = SandboxBuild(dict(self.context)).call()
        
        if response['status'] < 0:
            msg = ("Une erreur s'est produit c'est produite sur la sandbox (exit code: %d, env: %s)."
                   + " Merci de prévenir votre professeur.") % (response['status'], response['id'])
            if self.activity_session.user.profile.can_load():
                msg += "<br><br>" + htmlprint.code(response['sandboxerr'])
            raise Exception(msg)
        
        if response['status'] > 0:
            msg = ("Une erreur s'est produite lors de l'exécution du script before/build "
                    + ("(exit code: %d, env: %s). Merci de prévenir votre professeur"
                       % (response['status'], response['id']))
                  )
            if self.activity_session.user.profile.can_load() and response['stderr']:
                msg += "<br><br>Reçu sur stderr:<br>" + htmlprint.code(response['stderr'])
            raise Exception(msg)
        
        self.envid = response['id']

        
        context = dict(response['context'])
        keys = list(response.keys())
        for key in keys:
            response[key+"__"] = response[key]
        for key in keys:
            del response[key]
        del response['context__']
        
        context.update(response)
        self.context.update(context)
        self.built = True
        self.save()
    
    
    def get_navigation(self, request, context=None):
        pl_list = []
        pl_list.append({
                'id'   : None,
                'state': None,
                'title': self.activity_session.activity.pltp.json['title'],
        })
        for pl in self.activity_session.activity.pltp.pl.all():
            pl_list.append({
                'id'   : pl.id,
                'state': Answer.pl_state(pl, self.activity_session.user),
                'title': pl.json['title'],
            })
        context = dict(self.context if not context else context)
        context.update({
            "pl_list__": pl_list,
            'pl_id__': self.pl.id if self.pl else None
        })
        return get_template("playexo/navigation.html").render(context, request)
    
    
    def get_exercise(self, request, context=None):
        pl = self.pl
        seed = Answer.last_seed(pl, self.activity_session.user)
        if 'oneshot' in self.context or not seed or Answer.last_success(pl, self.activity_session.user) == True :
            seed = time.time()
            self.built = False
        self.add_to_context('seed', seed)
        
        
        if pl:
            if not context:
                if not self.built:
                    self.build()
                dic = dict(self.context)
            else:
                dic = dict(context)
            dic['user_settings__'] = self.activity_session.user.profile
            dic['user__'] = self.activity_session.user
            dic['pl_id__'] = pl.id
            dic['answers__'] = Answer.last_answer(pl, self.activity_session.user)
            for key in dic:
                dic[key] = Template(dic[key]).render(RequestContext(request, dic))
            return get_template("playexo/pl.html").render(dic)
        
        else:
            dic = dict(self.context if not context else context)
            dic['user_settings__'] = self.activity_session.user.profile
            dic['user__'] = self.activity_session.user
            dic['first_pl__'] = self.activity_session.activity.pltp.pl.all()[0].id
            for key in dic:
                dic[key] = Template(dic[key]).render(RequestContext(request, dic))
            return get_template("playexo/pltp.html").render(dic, request)
    
    
    def get_context(self, request, context=None):
        return {
            "navigation": self.get_navigation(request, context),
            "exercise": self.get_exercise(request, context),
        }



class Answer(models.Model):
    answers = JSONField(default='{}')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pl = models.ForeignKey(PL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)
    seed = models.CharField(max_length=100, default=time.time)
    date = models.DateTimeField(default=timezone.now)
    grade = models.IntegerField(null=True)
    
    
    @staticmethod
    def last_seed(pl, user):
        answers = Answer.objects.filter(pl=pl, user=user).order_by("-date")
        return None if not answers else answers[0].seed
    
    
    
    @staticmethod
    def last_success(pl, user):
        answers = Answer.objects.filter(pl=pl, user=user).order_by("-date")
        return False if not answers or answers[0].grade is None else answers[0].grade > 0
    
    
    
    @staticmethod
    def last_answer(pl, user):
        answers = Answer.objects.filter(pl=pl, user=user).order_by("-date")
        return {} if not answers else answers[0].answers
    
    
    @staticmethod
    def pl_state(pl, user):
        """Return the state of the answer with the highest grade."""
        answers = Answer.objects.filter(user=user, pl=pl).order_by("-grade")
        return State.NOT_STARTED if not answers else State.by_grade(answers[0].grade)
    
    
    @staticmethod
    def pltp_state(pltp, user):
        """Return a list of tuples (pl_id, state) where state follow pl_state() rules."""
        return [(pl.id, Answer.pl_state(pl, user)) for pl in pltp.pl.all()] 
    
    
    @staticmethod
    def pltp_summary(pltp, user):
        """
            Give information about the PLTP's completion of this user as a dict of 5 lists:
            {
                'succeeded':   [ % succeeded, nbr succeeded],
                'part_succ':   [ % part_succ, nbr part_succ],
                'failed':      [ % failed, nbr failed],
                'started:      [ % started, nbr started],
                'not_started': [ % not started, nbr not started],
            }
        """
        
        state = {
            State.SUCCEEDED:   [0.0, 0],
            State.PART_SUCC:   [0.0, 0],
            State.FAILED:      [0.0, 0],
            State.STARTED:     [0.0, 0],
            State.NOT_STARTED: [0.0, 0],
        }
        
        for pl in pltp.pl.all():
            state[
                State.STARTED if Answer.pl_state(pl, user) in [State.TEACHER_EXC, State.SANDBOX_EXC] else Answer.pl_state(pl, user)
                ][1] += 1
            
        nb_pl = sum([state[k][1] for k in state]) 
        nb_pl = 1 if not nb_pl else nb_pl
        
        for k, v in state.items():
            state[k] = [str(state[k][1]*100/nb_pl), str(state[k][1])]
        
        return state
    
    
    @staticmethod
    def course_state(course):
        """ 
            Return every pltp state of every user of this course as a list of dicts:
            {
                'user_id': id,
                'pltp_sha1' sha1,
                'pl': list(pl_id, state)
            }
            where 'state' follow pl_state() rules.
        """
        
        lst = list()
        for user in course.user:
            dct = dict()
            dct['user_id'] = user.id
            for activity in course:
                dct['pltp_sha1'] = activity.pltp.sha1
                dct['pl'] = Answer.pltp_state(activity.pltp, user)
            lst.append(dct)
        
        return lst
    
    
    @staticmethod
    def user_course_summary(course, user):
        """
            Give information about the completion of every PL of this user in course as a dict of 5 tuples:
            {
                'succeeded':   [ % succeeded, nbr succeeded],
                'part_succ':   [ % part_succ, nbr part_succ],
                'failed':      [ % failed, nbr failed],
                'started:      [ % started, nbr started],
                'not_started': [ % not started, nbr not started],
            }
        """
    
        state = {
            State.SUCCEEDED:   [0.0, 0],
            State.PART_SUCC:   [0.0, 0],
            State.FAILED:      [0.0, 0],
            State.STARTED:     [0.0, 0],
            State.NOT_STARTED: [0.0, 0],
        }
        
        for activity in course.activity.all():
            summary = Answer.pltp_summary(activity.pltp, user)
            for k in summary:
                state[k][1] += int(summary[k][1])
        
        nb_pl = sum([state[k][1] for k in state]) 
        nb_pl = 1 if not nb_pl else nb_pl
        
        for k, v in state.items():
            state[k] = [str(state[k][1]*100/nb_pl), str(state[k][1])]
        
        return state
