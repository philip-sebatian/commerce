from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import AuctionListing,bid,comments,User,watchlist,closelisting,category
from django.contrib.auth.decorators import login_required


from .models import User


def index(request):
    return render(request, "auctions/index.html",{
        'items':AuctionListing.objects.filter(status="active"),"range":range(1,len(AuctionListing.objects.filter(status="active"))+1)
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
@login_required(login_url='login')
def listing(request,id):
    if request.method=="POST":
        return render(request,'auctions/listing.html',{
            'item':AuctionListing.objects.get(id=id),'comments':comments.objects.filter(item=AuctionListing.objects.get(id=id)),'c_bid':bid.objects.get(item=AuctionListing.objects.get(id=id)),'watchlist':watchlist.objects.filter(item=AuctionListing.objects.get(id=id),user=request.user).exists(),
            'closelisting':AuctionListing.objects.get(id=id).owner==request.user
        })
    return render(request,'auctions/listing.html',{
            'item':AuctionListing.objects.get(id=id),'comments':comments.objects.filter(item=AuctionListing.objects.get(id=id)),'c_bid':bid.objects.get(item=AuctionListing.objects.get(id=id)),'watchlist':watchlist.objects.filter(item=AuctionListing.objects.get(id=id),user=request.user).exists(),
            'closelisting':AuctionListing.objects.get(id=id).owner==request.user
        })
@login_required(login_url='login')
def comment(request,id):
    if request.method=='POST':
        data=request.POST
        com_ment=data['comment']
        item=AuctionListing.objects.get(id=id)
        f=comments(item=item,comments=com_ment,comments_owner=request.user)
        f.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))
@login_required(login_url='login')
def bids(request,id):
    if request.method=='POST':
        data=request.POST
        item=AuctionListing.objects.get(id=id)
        current_bid=data['current_bid']
        f=bid.objects.get(item=item)
        f.bidding=current_bid
        f.highestbider=request.user
        f.save()
        return HttpResponseRedirect(reverse("listing",args=[id]))
@login_required(login_url='login')
def create(request):
    category_choice=[
    'Food',
    'Vehicles',
    "Electronics",
    "Cloths",
    'Books',
    "Others"
]
    if request.method=="POST":
        data=request.POST
        item=data['item']
        desc=data['desc']
        price=data['price']
        img=data['img']
        Category=data["categories"]
        f=AuctionListing(item=item,listingprice=price,description=desc,owner=request.user,img=img,Category=Category)
        f.save()
        x=bid(item=f,bidding=price,highestbider=request.user)
        x.save()
        

        return HttpResponseRedirect(reverse('index'))
    return render(request,"auctions/create.html",{
        "category":category_choice
    })


@login_required(login_url='login')
def Watchlist(request):
    if request.method=="POST":
        data=request.POST
        id=data['id']
        f=AuctionListing.objects.get(id=id)
        if not watchlist.objects.filter(item=f,user=request.user):
            watchlistitem=watchlist(item=f,user=request.user)
            watchlistitem.save()
        return render(request,"auctions/watchlist.html",{
            'watchlist':watchlist.objects.filter(user=request.user)
        })
    return render(request,"auctions/watchlist.html",{
        'watchlist':watchlist.objects.filter(user=request.user)
    })

@login_required(login_url='login')
def deletewatch(request):
    if request.method=='POST':
        data=request.POST
        itemid=data['item']
        watchlist.objects.get(item=itemid,user=request.user).delete()
        return HttpResponseRedirect(reverse('watchlist'))
@login_required(login_url='login')   
def closelistings(request):
    if request.method=="POST":
        data=request.POST
        id =data['id']
        f=AuctionListing.objects.get(id=id)
        f.status='closed'
        f.save()
        x=closelisting(item=f,winner=bid.objects.get(item=f).highestbider)
        x.save()
        return render(request,'auctions/closelisting.html',{
            "closelisting": closelisting.objects.all()
        })
    
    return render(request,'auctions/closelisting.html',{
            "closelisting": closelisting.objects.all()
        })



def Categories(request):
    category_choice=[
    'Food',
    'Vehicles',
    "Electronics",
    "Cloths",
    'Books',
    "Others"
]
    return render(request,'auctions/categories.html',{
        'category':category_choice
    })

def viewcat(request):
    if request.method=="POST":
        data=request.POST
        cat=data['categories']
        f=AuctionListing.objects.filter(Category=cat,status="active")
        return render(request,"auctions/viewcat.html",{
            'items':f ,"cat":cat
        })
