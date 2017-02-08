from django.test import TestCase

from .models import Prediction, Station

# Create your tests here.

"""
Tests for the Prediction model.
"""
class PredictionTests(TestCase):

    def test_prediction_creation(self):
        test_station = Station(station_name="Test Station", station_address="100 Test St.")
        # test this is valid input
        self.assertIsInstance(Station(station=test_station, bikes_available=4.87, day_of_week="Mon", start_hour=5), Station)
        # test invalid inputs
        with self.assertRaises(Exception):
            test_station = Station(station=test_station, bikes_available=4.87, day_of_week="Monday", start_hour=5)
        with self.assertRaises(Exception):
            test_station = Station(station=test_station, bikes_available=4.87, day_of_week="Monday", start_hour=25)
        with self.assertRaises(Exception):
            test_station = Station(station=test_station, bikes_available=4.87, day_of_week="Mon", start_hour=-4)
        with self.assertRaises(Exception):
            test_station = Station(station=test_station, bikes_available=-4.3, day_of_week="Mon", start_hour=5)