# DivAssist
This is DivAssist!  A webapp companion to the Divvy Bikeshare service.  
  
### How to Run
Navigate to the primary project folder divassist/ (make sure you are in the same directory as Makefile)  
To start the server:  
`make run`  
To run the tests:  
`make tests`


### Suggested Acceptance Tests  
##### 1. User Authentication
* Logging in with username="marlon" and password="marlon" should be successful because this accouent has already been registered. You will be navigated to your home page.
* Logging in with username="nonexistent" and password="aaa" should not be successful. An error message saying that username and password do not match will pop up.
* Clicking on the "Register" hyperlink will navigate you to the account creation page.
* On the account creation page, creating an account with username="marlon" should not be successful. An error message saying that the username has been taken will pop up.
* On the account creation page, creating an account with password="a" and password(again)="aa" should not be successful. An error message saying that the two passwords are not the same will pop up.  
* On the account creation page, creating an account with email="a" should not be successful. An error message saying that you should enter a valid email address will pop up.  
* On the account creation page, creating an account with username="newuser", email="a@gmail.com",  password="aa" and password(again)="aa" should be successful. You will be navigated to the home station selection page.  
* On the home station selection page, clicking on the "Save & Continue" button will navigate you to your homepage.  

##### 2. On User Homepage
* On your homepage, clikcing on the "View Rides" button will navigate you to the ride-viewing page.
* On your homepage, clikcing on the "Search Ride" button will navigate you to the ride-searching page.
* On your homepage, clikcing on the "Upload Ride" button will navigate you to the ride-adding page.
* On your homepage, clikcing on the "Logout" button on the top right cornet will make you logout and navigate you to the initial login page.

### Current Progress  


### How We Split the Work  


### Changes Since Previous Milestone  


### Others  
