from django.test import TestCase, Client
from django.utils import timezone
from .models import Station, UserProfile, Ride, Tag, Stop, Ride_Review, Station_Review, Ride_Rating, Station_Rating, User, Prediction

# Create your tests here.

class UserAuthenticationTests(TestCase):
    def set_up(self):
        self.client = Client()

    def test_template_availability(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/register/').status_code, 200)
        self.assertEqual(self.client.get('/registration/select_home_station/').status_code, 200)
        # login required pages are not available
        self.assertEqual(self.client.get('/home_page/').status_code, 302)

    def test_user_creation(self):
        test_client = Client()
        # registration arguments are invalid, page should not redirect
        # if two passwords are not the same
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': 'a@gmail.com', 
                                                   'password1': 'tomtom2', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 200);
        # if email address seems invalid
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': 'a', 
                                                   'password1': 'tomtom', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 200);
        # if any field is empty
        response = test_client.post('/register/', {'username': '', 
                                                   'email': 'a@gmail.com', 
                                                   'password1': 'tomtom', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 200);
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': '', 
                                                   'password1': 'tomtom', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 200);
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': 'a@gmail.com', 
                                                   'password1': '', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 200);
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': 'a@gmail.com', 
                                                   'password1': 'tomtom2', 
                                                   'password2': ''})
        self.assertEqual(response.status_code, 200);

        # page should direct if all arguments are valid
        response = test_client.post('/register/', {'username': 'tom', 
                                                   'email': 'a@gmail.com', 
                                                   'password1': 'tomtom', 
                                                   'password2': 'tomtom'})
        self.assertEqual(response.status_code, 302);
        self.assertRedirects(response, '/registration/select_home_station/')

    def test_login(self):
        # create a user for testing
        user = User()
        user.username = 'test'
        user.set_password('pass')
        user.save()

        test_client = Client()
        # user cannot login with incorrect username-password pair
        response = test_client.post('/', {'username': 'test', 'password': 'notpass'})
        self.assertEqual(response.status_code, 200)
        response = test_client.post('/', {'username': '', 'password': 'notpass'})
        self.assertEqual(response.status_code, 200)
        response = test_client.post('/', {'username': 'test', 'password': ''})
        self.assertEqual(response.status_code, 200)
        # user can login with correct username-password pair
        response = test_client.post('/', {'username': 'test', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home_page/')

    def test_logout(self): 
        # create a user for testing
        user = User()
        user.username = 'test'
        user.set_password('pass')
        user.save()

        test_client = Client()
        test_client.login(username='test', password='pass')
        response = test_client.get('/home_page/')
        self.assertEqual(response.status_code, 200)
        test_client.get('/logout/')
        # client should not be able to access home_page directly after logout
        response = test_client.get('/home_page/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/?next=/home_page/')


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
        # test stations
        station = Station(station_name="Ellis", station_address="59th and Ellis")
        station.save()
        s = Stop(ride=r, number=1, station=station)
        s.save()
        self.assertIs(Stop.objects.get(ride=r), [s])
        self.assertIs(Stop(ride=r, number=1, station=station), False) # you cannot have multiple stops with the same number
        self.assertIs(Stop(ride=r, number=3, station=station), False) # you cannot skip a number
        self.assertIs(Stop(ride=r, number=2, station=station), True) # you can have the same stop multiple times
        self.assertIs(Ride_Review.objects.get(ride=r), [])
        rr1 = Ride_Review(ride=r, comment="This was great", pub_date=timezone.now())
        rr1.save()
        user = User()
        user.username = 'test'
        user.set_password('pass')
        user.save()

        self.assertIs(Ride_Review.objects.get(ride=r), [rr1])
        self.assertIs(Ride_Rating(ride=r, rating=11, owner=u1), False)
        self.assertIs(Ride_Rating(ride=r, rating=-1, owner=u1), False)
        self.assertIs(Ride_Rating(ride=r, rating=4, owner=u1), True)
        rating = Ride_Rating(ride=r, rating=4, owner=u1)
        rating.save()
        self.assertIs(r.averageRating(), 4)
    def test_stations(self):
        station = Station(station_name="Ellis", station_address="59th and Ellis")
        station.save()
        user = User()
        user.username = 'test'
        user.set_password('pass')
        user.save()
        u1 = UserProfile(user=user, email="me@me.com")
        u1.save()
        st = Station_Rating(station=station, rating=7, owner=u1)
        st.save()
        st1 = Station_Rating(station=station, rating=2, owner=u1)
        st1.save()
        self.assertIs(station.averageRating(), 2) # it should overwrite
        self.assertIs(Station_Rating(station=station, rating=22, owner=u1), False)
        self.assertIs(Station_Rating(station=station, rating=-3, owner=u1), False)
        self.assertIs(Station_Rating(station=station, rating=3, owner=u1), True)

        # Station Reviews
        st = Station_Review(station=station, comment="LOUSY", pub_date=timezone.now(), owner=u1)
        st.save()
        st1 = Station_Review(station=station, comment="AMAZING", pub_date=timezone.now(), owner=u1)
        st1.save()
        self.assertIs(Station_Review.object.filter(station=station), [st, st1]) # it should not overwrite
        self.assertIs(Station_Review(station=station, comment="THE BEST", pub_date=timezone.now(), owner=u1), True)


class PredictionTests(TestCase):
    def test_prediction_creation(self):
        test_station = Station(station_name="Test Station", station_address="100 Test St.")
        test_station.save()
        # test model initialization and saving
        test_prediction = Prediction(station=test_station, bikes_available=4.87, day_of_week="Mon", start_hour=5)
        test_prediction.save()
        # test setters
        # set day_of_week
        self.assertFalse(test_prediction.set_day_of_week("Mond")) # invalid day
        self.assertTrue(test_prediction.set_day_of_week("Wed")) # valid day
        self.assertIs(test_prediction.day_of_week, "Wed") # check setter worked
        # set start_hour
        self.assertFalse(test_prediction.set_start_hour(24)) # invalid hour
        self.assertFalse(test_prediction.set_start_hour(-1)) # invalid hour
        self.assertTrue(test_prediction.set_start_hour(23)) # valid hour
        self.assertIs(test_prediction.start_hour, 23) # check setter worked
        # set bikes_available
        self.assertFalse(test_prediction.set_bikes_available(-0.1)) # invalid num bikes
        self.assertTrue(test_prediction.set_bikes_available(2.98)) # valid num bikes
        self.assertIs(test_prediction.bikes_available, 2.98) # check setter worked