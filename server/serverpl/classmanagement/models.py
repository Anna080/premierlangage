import logging

from django.db import models
from django.contrib.auth.models import User

from lti_app.models import LTIModel
from user_profile.enums import Role


logger = logging.getLogger(__name__)


class Course(LTIModel):
    teacher = models.ManyToManyField(User, related_name="teaches", blank=True)
    student = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=20)
    
    @classmethod
    def get_or_create_from_lti(cls, user, lti_launch):
        """Create a Course corresponding to the ressource in the LTI request.
        
        Returns a tuple of (object, created), where object is the retrieved or created object and
        created is a boolean specifying whether a new object was created.

        Return None, False if parameters are missing in lti_launch."""
        course_id = lti_launch["context_id"]
        course_name = lti_launch.get("context_title")
        course_label = lti_launch.get("context_label")
        consumer = lti_launch['oauth_consumer_key']
        if not (course_id and course_name and course_label and consumer):
            return None, False

        try:
            course = cls.objects.get(consumer_id=course_id, consumer=consumer)
            created = True
        except cls.DoesNotExist:
            course = cls.objects.create(consumer_id=course_id, consumer=consumer,
                                        name=course_name, label=course_label)
            logger.info("New course created: %d - '%s' (%s:%s)"
                        % (course.pk, course.name, consumer, course_id))
            created = False
            
        course.student.add(user)
        for role in lti_launch["roles"]:
            if role in ["urn:lti:role:ims/lis/Instructor", "Instructor"]:
                course.teacher.add(user)
        course.save()
        
        return course, created
    
    
    def is_member(self, user):
        """Return True if the user is a member of the course (student or teacher), False if not."""
        return user in self.teacher.all() or user in self.student.all()
    
    
    def is_teacher(self, user):
        """Return True if the user is a teacher of the course."""
        return user in self.teacher.all() and user.profile.role <= Role.INSTRUCTOR
    
    
    def __str__(self):
        return str(self.id) + ": [" + self.label + "] " + self.name
