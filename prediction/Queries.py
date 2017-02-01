"""
Exception for when an undefined query tries to be run
"""
class UndefinedQueryError(Exception):
    pass

"""
Exception for when a query doesn't receive its expected args
"""
class ArgMissingError(Exception):
    pass

"""
Base class for a Divvy query
"""
class DivvyQuery():

    def __init__(self, spark_interface):
        self.spark_interface = spark_interface
        self.spark_interface.data.createOrReplaceTempView("divvyData")

    def run(self, args):
        raise UndefinedQueryError()

"""
Query that gets the average number of bikes at a station during a given time window

Expects args to run:
    - station: String of a valid station name
    - start_hour: Integer between 0 and 24
    - end_hour: Integer between 0 and 24
"""
class AverageBikesByHour(DivvyQuery):
    def run(self, args):
        # args check
        expected_args = ["station", "start_hour", "end_hour"]
        for exp in expected_args:
            if exp not in args:
                raise ArgMissingError("Expected arg: " + exp)

        startT, endT = args["start_hour"], args["end_hour"]

        aveQuery = "HOUR(Timestamp) BETWEEN {} and {}".format(startT,endT)
        aveAvailable = self.spark_interface.sqlc.sql("SELECT * FROM divvyData WHERE Station_Name LIKE '{}' AND {}".format(args["station"], aveQuery))
        return aveAvailable.groupBy("Station_Name").avg("Available_Bikes")

"""
Query that gets the average number of bikes at a station during a given time window

Expects args to run:
    - station: String of a valid station name
    - start_hour: Integer between 0 and 24
    - end_hour: Integer between 0 and 24
    - day: String of a three-letter day (e.g. Mon, Tue, Wed)
"""
class AverageBikesByDayAndHour(DivvyQuery):
    def run(self, args):
        # args check
        expected_args = ["station", "start_hour", "end_hour", "day"]
        for exp in expected_args:
            if exp not in args:
                raise ArgMissingError("Expected arg: " + exp)

        locSpec = "Station_Name LIKE '{}'".format(args["station"])
        timeSpec = "HOUR(Timestamp) BETWEEN {} and {} ".format(args["start_hour"],args["end_hour"])
        daySpec = "date_format(Timestamp,'E') LIKE '{}'".format(args["day"])
        ave = self.spark_interface.sqlc.sql("SELECT * FROM divvyData WHERE {} AND {} AND {}".format(locSpec,timeSpec,daySpec))

        return ave.groupBy("Station_Name").avg("Available_Bikes")