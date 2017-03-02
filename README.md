# DivAssist
This is DivAssist!  A webapp companion to the Divvy Bikeshare service.  
  
### How to Run
Navigate to the primary project folder divassist/ (make sure you are in the same directory as Makefile)  
To start the server:  
`make run`  
To run the tests:  
`make tests`

In order to be able to view the Prediction page, you need to set the `GOOGLE_MAPS_KEY` environment variable to a valid [Google Maps Javascript API Key](https://developers.google.com/maps/documentation/javascript/get-api-key). You can do so (for your current shell) by running:

`export GOOGLE_MAPS_KEY=YOUR_API_KEY`

### Suggested Acceptance Tests  
##### 1. User Authentication
* Clicking on the "Register" hyperlink will navigate you to the account creation page.
* On the account creation page, creating an account with username="marlon" should not be successful. An error message saying that the username has been taken will pop up.
* On the account creation page, creating an account with password="a" and password(again)="aa" should not be successful. An error message saying that the two passwords are not the same will pop up.  
* On the account creation page, creating an account with email="a" should not be successful. An error message saying that you should enter a valid email address will pop up.  
* On the account creation page, creating an account with username="newuser", email="a@gmail.com",  password="aa" and password(again)="aa" should be successful. You will be navigated to the home station selection page.  
* On the home station selection page, clicking on the "Save & Continue" button will navigate you to your homepage.  
* On your homepage, clikcing on the "Logout" button on the top right cornet will make you logout and navigate you to the initial login page.  

* Now after making sure that you are on the login page: 
* Logging in with username="nonexistent" and password="aaa" should not be successful. An error message saying that username and password do not match will pop up.
* Logging in with username="newuser" and password="aa" should be successful because this accouent has already been registered. You will be navigated to your home page.

* Now after making sure that you are on the login page: 
* Logging in with username="nonexistent" and password="aaa" should not be successful. An error message saying that username and password do not match will pop up.
* Logging in with username="newuser" and password="aa" should be successful because this accouent has already been registered. You will be navigated to your home page.

* After logging in navigate to the rides/add_ride and add a ride with all the parameters.
* Go to search and enter a variety of potential search terms.  All data is dummy data.

##### 2. On User Homepage
* On your homepage, clicking on the "View Rides" button will navigate you to the ride-viewing page.
* On your homepage, clicking on the "Search Ride" button will navigate you to the ride-searching page.
* On your homepage, clicking on the "Upload Ride" button will navigate you to the ride-adding page.

### Current Progress  
* We have finished implementing mechanism for a user to create an account, login, and logout. Basically we have finished the entire activity diagram on page 7 of our writeup, except that the functionality for selecting home stations has not yet been implemented.
* We have finished implementing the navigation logic between different web pages. The activity diagram on page 8 has been fully implemented, except that some of the leaf pages like "browse rides" and 'view saved stations' are using dummy data.
* We have implemented partial functionality to create a ride.  The functionality is complete with authentication and parsing without a list of rides or stations.
* The search functionality is implemented by difficulty, start neighborhood, end neighborhood, or some combination of those.
* Predictions was further implemented

### How We Split the Work  
1. Marlon Liu, Joshua Liu, and Paulo Nascimento formed a group to work on user registration and authentication, and the user's homepage.

   Marlon: 
   - the backend for structure for user authentication. Mainly registration forms and how these forms will be handled.  
   - the navigation logic between pages
   - fetching data from the cityofchicago data portal  

   Joshua:
   - designing the entire UI/UX component for this webapp
   - all css and beginning html files

2. Hannah Brodheim and Gaibo Zhang formed a group to work on rides pages.

   Gaibo:
   - Added templates and views for searching, creating, and viewing rides
   
   Hannah:
   - Added and incorporated with Gaibo views functionality for updating, creating, and searching rides

3. Rob and Ben worked on the predictions framework.  Together they populated the predictions and added base methods to use the class as    required by the tests previously written.

### Changes Since Previous Milestone  


### Others  
