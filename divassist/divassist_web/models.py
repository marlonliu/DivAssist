from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    home_station_1 = models.ForeignKey(Station)
    home_station_2 = models.ForeignKey(Station)
    home_station_3 = models.ForeignKey(Station)
    
    def __str__(self):
        return self.user
    
class Ride(models.Model):
    title_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    desc_text = models.CharField('description', max_length=2000)
    s_neighborhood = models.CharField('start neighborhood', max_length=200)
    e_neighborhood = models.CharField('end neighborhood', max_length=200)
    difficulty = models.IntegerField()
    owner = models.ForeignKey(User)

# A ride can have many tags
# A tag can be associated with many rides
class Tag(models.Model):
    rides = models.ManyToManyField(Ride)
    tag = models.CharField(max_length=20)

# A ride has a sequence of stations
class Stop(models.Model):
    ride = models.ForeignKey(Ride)
    number = models.IntegerField()
    station = models.ForeignKey(Station)

# A review has a comment an owner and a date
class Ride_Review(models.Model):
    ride = models.ForeignKey(Ride)
    comment = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date commented')
    owner = models.ForeignKey(User)

# A review has a comment an owner and a date
class Station_Review(models.Model):
    station = models.ForeignKey(Station)
    comment = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date commented')
    owner = models.ForeignKey(User)

# Every user should only rate once
# Each should be associated with one ride
class Ride_Rating(models.Model):
    ride = models.ForeignKey(Ride)
    rating = IntegerField(default=0)
    owner = models.ForeignKey(User)

# Every user should only rate once
# Each should be associated with one ride
class Station_Rating(models.Model):
    station = models.ForeignKey(Station)
    rating = IntegerField(default=0)
    owner = models.ForeignKey(User)

class Station(models.Model):
    station_id = models.IntegerField()
    station_name = models.CharField(max_length=36)
    station_address = models.CharField(max_length=200)
