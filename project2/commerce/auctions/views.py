from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Listing, Bid, comment,  category
from django.contrib import messages
from django import forms
from .forms import ListingForm, BidForm, CommentForm


from .models import User


def index(request):
    return render(request, "auctions/index.html")


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

def create_listing(request):
    if request.method=="POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            Listing=form.save(commit=False)
            Listing.owner=request.user
            Listing.current_price=request.starding_bid
            Listing.save()
            messages.success(request,"Listing created successflly ")
            return redirect ("index")
    else:
        form=ListingForm()
        return render (request,"auctions/create_listing.html",{"form":form})
    
def listing_detail(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)
    bid_form=CommentForm()
    comment_form=CommentForm()
    return render (request, "auctions/listing_detail.html",{
        "listing":listing,
        "bild_form":bid_form,
        "comment_form":comment_form
    })

def place_bid(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)
    if request.method=="POST":
        form=BidForm(request.POST)
        if form.is_valid():
            bid=form.canceled_data["amount"]
            if bid>listing.current_price:
                Bid.objects.create(listing=listing, bidder=request.user ,amount=bid)
                listing.current_price=bid
                listing.save()
                messages.success(request,"Bid placed successfelly ")
            else:
                messages.error(request,"Your Bid must be higher than the current price")
    return redirect("listing_detail", listing_id=Listing.id)

def add_comment(request, listing_id):
    listing=get_object_or_404(Listing, id=listing_id)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.listing=listing
            comment.user=request.user 
            comment.save()
            messages.success(request,"comment added")
    return redirect ("listing_detail",listing_id=Listing.id)