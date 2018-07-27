# Project 1

Web Programming with Python and JavaScript

This README is arranged in order of requirements to facilitate the reading

(0. ) The layout html is basic page structure and all other layout files are extending it.
1. When user opens the site (and is not logged in) The index.html-layout is shown. It basically only contains the login form and link to the registration form.
   If user opens the registration form registrate.html is opened, containing fields for user name, email, login and password. When the user fills the form registration function adds the user to database (users table) and hashes password with argon2 (added to requirements.txt). Afterwards the user is forwarded to registration.html, which only tells that registration was successful.
2. If user is giving the right credentials to login form on the first page his user data is saved in session variable (user) and he/she is forwarded to logged.html. If the credentials were
   wrong he/she is re-forwarded to home page for new try.
3. If user clicks Log out-button on top right, the session variable is destroyed and user is redirected to the front page.
4. import.py is transferring the csv contents to the database books-table, skipping the first line (column headings), Nothing fancy there.
5. Search is facilitated by simple search form on the logged.html. When user makes a search the system is checking title, author and isbn columns with LIKE-function to handle the substring search.
   The search is currently case-sensitive, so authors' names should be correctly capitalized. Not a big deal to circumvent but as it wasn't required didn't do it (might be preferable to be case-sensitive!)
6. On the search results list there is a link named Details, which forwards the user to the details.html. On the page there are all basic information about the book, the reviews saved by
   the application and ratings visualized with golden stars by font-awesome. From the bottom of the page user is able to click back to the search page (logged.html)
7. The review is allowed if the user hasn't made a review on that book earlier, showing the form where to select the rating and write a review. The reviews are saved to a table called reviews
   in the database. After saving the review the user is redirected back to the details page. The rating is implemented with radio buttons and review with textarea.
8. The goodreads reviews are injected before reviews of this system giving just the number of ratings and average ratings for the book - or saying there are none.
9. API access tries to find the book from the database and if not, returns 404, otherwise it builds a dictionary object of (title, author, year, isbn, number of ratings and average rating)
   and outputs it in JSON format. The average rating was a bit difficult as it is returned with decimal type, which isn't supported on json, had to convert it to float.

I have skipped most of the (unrequested) checks (e.g. fields may be left empty and so on). I can do them, but I prefer to concentrate on the main aspects of the course and time is a constraint.
