from django.test import TestCase, Client
from django.utils import timezone
from .models import Station, UserProfile, Ride, Tag, Stop, Ride_Review, Station_Review, Ride_Rating, Station_Rating, User

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



# class RideTests(TestCase):
#     def test_ride_creation(self):
#         test_ride = Ride(title_text = "The Trip to Grandma's House", desc_text="It's so fun though guys!", s_neighborhood="Hyde Park", e_neighborhood="West Loop", difficulty=10)
#         self.assertIs(Ride(title_text="", desc_text=""), False)
#         r = Ride(title_text="Title", desc_text="Description", s_neighborhood="Hyde Park", e_neighborhood="West Loop", pub_date=timezone.now(), owner=UserProfile(), difficulty=9)
#         r.save()
#         self.assertIs(r.setDifficulty(11), False)
#         self.assertIs(r.getDifficulty(), 9)
#         self.assertIs(r.setDifficulty(-12), False)
#         self.assertIs(r.setTitle(""), False)
#         tag1 = Tag('Hilly')
#         tag1.save()
#         tag1.rides.add(r)
#         self.assertIs(r.getTags(), ['Hilly'])
#         self.assertIs(r.hasTag(tag1), True)
#         tag2 = Tag('Scenery')
#         tag2.save()
#         self.assertIs(r.hasTag(tag2, False))
