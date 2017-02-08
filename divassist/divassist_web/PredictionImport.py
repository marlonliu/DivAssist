import csv
from divassist_web.models import Station, Prediction
from django.core.exceptions import ObjectDoesNotExist

"""
Exception for when a row is read for a station that doesn't exist in the database.
"""
class StationDoesNotExist(Exception):
    pass

"""
This class is meant to stand alone as a helper for importing predictions.
"""
class PredictionImportHelper():

    def __init__(self, import_filename):
        self.import_filename = import_filename
    
    def run(self):
        with open(self.import_filename, 'rb') as import_file:
            reader = csv.DictReader(import_file)
            for row in reader:
                # try to get a station with a matching name
                try:
                    station = Station.objects.get(station_name=row['Station_Name'])
                except ObjectDoesNotExist:
                    raise StationDoesNotExist()
                
                bikes_available = float(row['Average_availability'])
                start_hour = int(row['Start_One_Hour_Window'])
                # try to find the prediction in the database
                try:
                    prediction = Prediction.objects.get(day_of_week=row['Day'], start_hour=start_hour, station=station)
                    # update the prediction to the new ValueError
                    prediction.bikes_available = bikes_available
                    prediction.save()
                except ObjectDoesNotExist:
                    # create a new prediction
                    prediction = Prediction(bikes_available=bikes_available, day_of_week=row['Day'], start_hour=start_hour, station=station)
                    prediction.save()