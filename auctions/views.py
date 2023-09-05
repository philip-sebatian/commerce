from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import AuctionListing,bid,comments,User
from django.contrib.auth.decorators import login_required


from .models import User


def index(request):
    return render(request, "auctions/index.html",{
        'items':AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request,id):
    if request.method=="POST":
        return render(request,'auctions/listing.html',{
            'item':AuctionListing.objects.get(id=id),'comments':comments.objects.filter(item=AuctionListing.objects.get(id=id)),'c_bid':bid.objects.get(item=AuctionListing.objects.get(id=id))
        })
    return render(request,'auctions/listing.html',{
            'item':AuctionListing.objects.get(id=id),'comments':comments.objects.filter(item=AuctionListing.objects.get(id=id)),'c_bid':bid.objects.get(item=AuctionListing.objects.get(id=id))
        })
@login_required
def comment(request,id):
    if request.method=='POST':
        data=request.POST
        com_ment=data['comment']
        item=AuctionListing.objects.get(id=id)
        f=comments(item=item,comments=com_ment,comments_owner=request.user)
        f.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))
@login_required
def bids(request,id):
    if request.method=='POST':
        data=request.POST
        item=AuctionListing.objects.get(id=id)
        current_bid=data['current_bid']
        f=bid.objects.get(item=item)
        f.bidding=current_bid
        f.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))
