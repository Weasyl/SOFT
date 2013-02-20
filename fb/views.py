from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.db.models import Q

from fb.models import *

def index(request):
    if request.method != "POST":
        return render_to_response("index.html", {}, context_instance=RequestContext(request))
        
    fa = request.POST.get("my_fa")
    weasyl = request.POST.get("my_weasyl")
    raw_watchlist = request.POST.get("watchlist")
    error = ""
    
    print fa, weasyl
    
    # Add the given account if it's not there
    existing = Account.objects.filter(fa=fa, weasyl=weasyl)
    if not existing:
        account = Account(fa=fa, weasyl=weasyl, ip=request.META["REMOTE_ADDR"])
        account.save()
        
    # Format the watchlist
    raw_watchlist = raw_watchlist.split("\n")
    watchlist = []
    overflow = ""
    for user in raw_watchlist:
        user = user.replace("\t", "")
        user = user.replace("\n", "")
        user = user.replace("\r", "")
        if len(user) < 3:
            continue
        if len(watchlist) > 200:
            overflow += user + "\n"
            continue
        user = user.split(" ")[-1].lower()
        watchlist.append(user)
        
    if overflow != "":
        error = "Too many users at once! Once you finish with the ones that were processed, the unprocessed users are still listed above."
    
    # Get the users
    users = Account.objects.filter(fa__in=watchlist).order_by('fa').values()
    try:
        print users[0]
    except:
        print "No users"
        
    data = []
    for name in watchlist:
        match = False
        temp = {"fa":name, "weasyl":"", "vouchers":0, id:0}
        for user in users:
            if name == user["fa"]:
                temp["weasyl"] = user["weasyl"]
                temp["vouchers"] = user["vouchers"]
                temp["id"] = user["id"]
                data.append(temp)
                temp = {"fa":name, "weasyl":"", "vouchers":0, id:0}
                match = True
                print "added", temp
        if temp["weasyl"] == "" and not match:
            data.append(temp)
            print "ADDED", temp
    
    return render_to_response("index.html", {"overflow":overflow, "error":error, "fa":fa, "weasyl":weasyl, "users":data, "results":True}, context_instance=RequestContext(request))
    
def vouch(request):
    fa_id = request.GET.get("fa_id")
    weasyl = request.GET.get("weasyl")
    
    # See if you vouched
    if (fa_id == ""):
        correct = Account(fa=weasyl, weasyl=weasyl)
        correct.save()
        fa_id = correct.id

    v = Voucher.objects.filter(ip=request.META["REMOTE_ADDR"], fa_id=fa_id)
    if len(v) == 0:
        vouch = Voucher(ip=request.META["REMOTE_ADDR"], fa_id=fa_id)
        vouch.save()
        account = Account.objects.filter(pk=fa_id)[0]
        account.vouchers += 1
        account.save()
        print "New vouch"
    else:
        print "Already vouched"
   
    return HttpResponse("You vouched")
    
def correct(request):
    fa = request.GET.get("fa")
    weasyl = request.GET.get("weasyl").split("/")[-1]
    correct = Account(fa=fa, weasyl=weasyl)
    correct.save()
    return HttpResponse("Correction Submitted")