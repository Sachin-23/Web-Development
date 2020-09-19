# Requirements


+ Registration - name, username, password 
+ Login - username, password
+ Logout - Ending Session 
+ import - create import.py which will import all the data from a csv file and add into the postgresql database, before that create tables
+ Search - if the user types ISBN number of the book, the title of a book, or the author of a book. website should display a list of possible matching results, or some sort of message if there were no matches. even the substring from the above should dislplay a list of matches. 
+ Book Page - redirect to the book pages with title, author, publication year, ISBN numbers
+ review submission - upto 5stars, text review
+ reviews from goodreads should be displayed in book page
+ API access - /api/\<isbn\> should return a json response


+ Hints
  + tables
    + users
    + books
    + reviews
  + log a user in \- using session `session["user_id"]`



---
+ users - user\_id, name, username, password
+ books - ISBN, title, author, year
+ reviews - user\_id, ISBN, rating, text-review 
