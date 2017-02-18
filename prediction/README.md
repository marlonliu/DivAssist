# DivAssist Prediction Engine

We use Apache Spark to parallelize and streamline our prediction process. While the Divvy dataset is over 12 Gb in size and constantly expanding, with Spark we can create city-wide predictions in seconds. We've also created Spark interface and query classes to simplify the procedure for interacting and requesting predictions. 

##How to Run:
In `interfaceDemo.py` we've outlined the general procedure for working with the Spark interface and query classes. By copying this framework, it's very simple to create queries of your own. 

##Integrating with the rest of DivAssist
While station-specific predictions can be calculated in seconds, city-wide predictions are also computed in seconds. For simplicity, we can precalculate daily predictions and use those in the main DivAssist interface, and as such, the majority of what's contained in this repo is back-end and support frameworks.
