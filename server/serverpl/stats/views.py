
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


import matplotlib.pyplot as plt
import mpld3

from playexo.models import Answer
import datetime

@login_required
def user(request):

    # Data access

    # the all shebang
    queryset = Answer.objects.all()
    i=1
    userdic={}
    datedic=Counter()
    for a in queryset :
        if a.user not in  userdic:
            userdic[a.user.id]=[]
        if a.grade and a.grade > -1 :
            sdate = datetime.datetime.strftime(a.date, "%Y/%m/%d")
            datedic[sdate] += 1
            userdic[a.user.id].append(sdate)



    plt.plot(list(datedic.values()))
    x = mpld3.fig_to_html(plt.gcf())
    return render(request, "stats/stats.html", {
        "show": x,
    })


@login_required
def tags(request):
    queryset = Answer.objects.all()
    tdic=Counter()
    dic="empty"
    for a in queryset :
        pl = a.pl
        dic = pl.json

        if "tag" in dic:
            lt = dic['tag'].split('|')
            for t in lt:
                tdic[t]+= 1
        else:
            tdic['NONE'] +=1
    return render(request, "stats/stats.html", {
        "show": str(tdic),
    })

@login_required
def datestats(request):
    # if not User :
    #     queryset = Answer.objects.all()
    # else:
    queryset = Answer.objects.filter(user= request.user)
    if len(queryset)<1:
        queryset = Answer.objects.all()
    datedic = Counter()
    gooddic = Counter()
    meandic = dict()
    for a in queryset :
        if a.date:
            sdate = datetime.datetime.strftime(a.date, "%Y/%m/%d")
            datedic[sdate] += 1
            if a.grade and a.grade > 0 :
                gooddic[sdate] += 1
            else:
                gooddic[sdate] += 0
    height = max(datedic.values())
    mean = ( sum(gooddic.values())/sum(datedic.values()))*height
    hzondic=dict()
    for k in gooddic.keys():
        meandic[k] = (gooddic[k]/datedic[k])*height
        hzondic[k]= mean

    plt.figure(num=plt.gcf().number, figsize=(12, 14))
    plt.gca().set_title( 'Tentatives et tentatives réussies ', fontsize=20)
    plt.plot(list(datedic.values()))
    plt.plot(list(gooddic.values()),"red")
    plt.plot(list(meandic.values()), "green")
    plt.plot(list(hzondic.values()), "green")

    x = mpld3.fig_to_html(plt.gcf())
    return render(request, "stats/stats.html", {
        "show": "coucou:"+x,
    })

class Counter(dict):
    def __missing__(self, key):
        return 0



    # answers = JSONField(default='{}')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # pl = models.ForeignKey(PL, on_delete=models.CASCADE)
    # activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)
    # seed = models.CharField(max_length=100, default=time.time)
    # date = models.DateTimeField(default=timezone.now)
    # grade = models.IntegerField(null=True)
