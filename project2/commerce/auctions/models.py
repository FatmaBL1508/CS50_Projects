from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    starting_bid=models.DecimalField(max_digits=10, decimal_places=2)
    image_url=models.URLField(blank=True,null=True)
    category=models.CharField(max_length=50,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE,related_name="Listing")

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="bids")
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="bidders")
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} $ on {self.listing.title}"

class comment(models.Model):
     listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")
     user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenters")
     text=models.TextField()
     timestamp=models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"comment by{self.user.username}on {self.Listing.title}"
    
class watchlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="watchlist")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="watchers")

    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"
