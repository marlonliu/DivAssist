from os import listdir, environ

"""
Setup Django if file is run as a script
"""
if __name__ == '__main__':
    # check that the django environment var is set
    varval = "divassist.settings"
    try:
        assert environ['DJANGO_SETTINGS_MODULE'] == varval
    except KeyError, AssertionError:
        raise Exception("Ensure the DJANGO_SETTINGS_MODULE environment variable is \"{}\"".format(varval))
    
    # set up django
    import django
    django.setup()

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

    def __init__(self, import_directory):
        self.import_directory = import_directory
    
    def run(self):
        stations_created = 0
        predictions_created = 0
        predictions_updated = 0
        total_imports = 0
        for import_filename in listdir(self.import_directory):
            import_filepath = '/'.join([self.import_directory, import_filename])
            print "Importing {}...".format(import_filepath)
            with open(import_filepath, 'rb') as import_file:
                reader = csv.reader(import_file)
                for row in reader:
                    # try to get a station with a matching name
                    try:
                        station = Station.objects.get(station_name=row[0])
                    except ObjectDoesNotExist:
                        station = Station(station_name=row[0], station_address=row[0])
                        station.save()
                        stations_created += 1
                    
                    bikes_available = float(row[3])
                    start_hour = int(row[1])
                    # try to find the prediction in the database
                    try:
                        prediction = Prediction.objects.get(day_of_week=row[2], start_hour=start_hour, station=station)
                        # update the prediction to the new value
                        prediction.bikes_available = bikes_available
                        prediction.save()
                        predictions_updated += 1
                    except ObjectDoesNotExist:
                        # create a new prediction
                        prediction = Prediction(bikes_available=bikes_available, day_of_week=row[2], start_hour=start_hour, station=station)
                        prediction.save()
                        predictions_created += 1
        
        print "Created {} Stations".format(stations_created)
        print "Created {} Predictions".format(predictions_created)
        print "Updated {} Predictions".format(predictions_updated)

"""
Run the import if the file is run as a script.
"""
if __name__ == '__main__':
    p = PredictionImportHelper('divassist_web/predictions')
    p.run()