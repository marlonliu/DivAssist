from django.test import TestCase
from django.utils import timezone
from .models import Station, UserProfile, Ride, Tag, Stop, Ride_Review, Station_Review, Ride_Rating, Station_Rating

# Create your tests here.

class RideTests(TestCase):
    def test_ride_creation(self):
        test_ride = Ride(title_text = "The Trip to Grandma's House", desc_text="It's so fun though guys!", s_neighborhood="Hyde Park", e_neighborhood="West Loop", difficulty=10)
        self.assertIs(Ride(title_text="", desc_text=""), False)
        r = Ride(title_text="Title", desc_text="Description", s_neighborhood="Hyde Park", e_neighborhood="West Loop", pub_date=timezone.now(), owner=UserProfile(), difficulty=9)
        r.save()
        self.assertIs(r.setDifficulty(11), False)
        self.assertIs(r.getDifficulty(), 9)
        self.assertIs(r.setDifficulty(-12), False)
        self.assertIs(r.setTitle(""), False)
        tag1 = Tag('Hilly')
        tag1.save()
        tag1.rides.add(r)
        self.assertIs(r.getTags(), ['Hilly'])
        self.assertIs(r.hasTag(tag1), True)
        tag2 = Tag('Scenery')
        tag2.save()
        self.assertIs(r.hasTag(tag2, False))
