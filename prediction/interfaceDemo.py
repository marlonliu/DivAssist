from datetime import datetime
from SparkInterface import SparkInterface
import Queries as _q

s = SparkInterface()
args = {
    "station": "Museum Campus",
    "start_hour": 4,
    "end_hour": 5,
    "day": "Tue"
}

_q.AverageBikesByHour(s).run(args).show()
_q.AverageBikesByDayAndHour(s).run(args).show()