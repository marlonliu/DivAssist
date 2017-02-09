from django.test import TestCase

from .models import Prediction, Station

# Create your tests here.

"""
Tests for the Prediction model.
"""
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