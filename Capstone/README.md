## Final Project - Pedopt

Hello, World!
This is my project submission for CS50 Web programming with Python and Javascript
Final Project: Capstone

**Introduction**
+ My project is about Pet adoption and rehoming pet's. Users are able to search for a pet in there current location by pincode, city, or state and the kind of pet they are interested in by providing pet's type(dog, cat or other), age and sex. View pet's profile and details about the owner if they are interested in adopting the pet. Users can also add a pet to rehome.

+ The project was built using Django as a backend framework and JavaScript as a frontend programming language. All generated information are saved in database (SQLite by default).

Project Structure

+ `pedopt` - main application directory.
  + `static/pedopt` - contains all static content
    + `index.js` - contains Javascript used in the application.
      + Adding pet's profile to user's wishlist.
      + HTML Form Sanitation checking.
      + Pagination.
    + `style.css` - contains CSS, but for the most parts in the application I have used Bootstrap's css and tweaked with inline-css due to the CSS's precedence.
    + \*png & \*svg - photos and logo's.
  + `template/pedopt` - Contains all the applictaion template.
    + `Layout.html` - Base template. All other template extend it.
    + `index.html` - Main templates that show a search column(if user is signed in) and pet's profile
    + `login.html` - It shows login form for unregistered user.
    + `register.html` - It shows registeration form for unregistered user.
    + `profile.html` - This shows users wishlist and pets if the user has added to rehome. 
    + `get_pet.html` - Display single pet's profile with owner's details. 
    + `rehome.html` - Template for adding pets to rehome.
    +  `adopted.html` - This will display all the pets adopted.
  + `admin.py` - 
  + models.py - Contains three models
    + `User` - This model extends the standard User model.
    + `Pet` - model is for Pet and details about pet and it's owner.
    + `Wishlist` - Represents user's wishlist.
  + `urls.py` - all applications URL's.
  + `views.py` respectively, contains all application views.
+ `capstone` - project directory.
+ `media/images` - this directory contains the images uploaded by the user and the location is saved in database.

+ Functionalities

**Main Page**
  + Find a Pet
    + The default page of this web application will display recenlty added pets to rehome. 
    + Also users can search for the pets by \- location, pet type(Dog, Cat, Other), age, sex.

  + Pet Profile
    + Clicking on any of the pet, user will be redirected to the pet's profile 
    + If the user is the user who posted the pet's profile a button will displayed to remove from current rehoming to recently adopted.

+ Pet Profile
  + Pet's name, wishlist button, pet's image, fact about pet, pet's about (liking, about rehoming, and other things), Owner's Contact info will be displayed where the user can contact the user
  + Wishlist
    + User add pet to there and wishlist and remove if already added.

+ Rehome 
  + Here user can add a pet to rehome by filling up the form.

+ Recently Adopted
  + Adopted pets will be displayed.

+ Pages displaying pets card only 8 pets will be display to view next 8 next button will be displayed, if not on the first page previous button will be displayed.


**Justification**

This project is distinct from all previous projects so far. Why?
  + Completely Mobile responsive.
  + Uses Django's ModelForm.
  + Saving Images(location of the image) to Database.
  + Use of Paginations.
  + Adding Pets profile to Users wishlist using Ajax.
  + Finally this project is a combination of 9 weeks lessons and 5 assignments. 
