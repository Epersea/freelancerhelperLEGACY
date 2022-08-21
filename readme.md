# Freelancer Helper

[Video demo](https://youtu.be/_JCpaxIT-DQ)

## What is Freelancer Helper?
Freelancer Helper is a web application for freelancers who want to maximize their productivity.
As a freelancer myself, I know one of the most pressing questions, especially when starting out, is figuring out how much to charge. This website strives to provide an accurate answer to that through a **Rate Calculator** functionality. It also offers a **Client Tool** functionality, so the user can keep track of the profitability of their business in a per-client and global basis.
From a technology standpoint, this project uses the **Flask** framework, with Python, HTML and SQL as the main technologies. It builds on the code from CS50’s pset 9, Finance, building new and/or improved functionalities.
One of my main goals for this project was to keep my code organized, distributing the main functionalities in different files and trying to keep my functions small and readable.

## Project files

### `freelancer.db`
This is a simple **SQLite3** database with three different tables: users, rates and clients. The three tables are cross-referenced by the user ID. This is the full database schema:
```
CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, hash TEXT, minimum_rate REAL);
CREATE TABLE rates (id INTEGER PRIMARY KEY, user_id INTEGER, rate REAL, annual_expenses REAL, hours_day REAL, billable_hours_year REAL, billable_percent REAL, net_month REAL, tax_percent REAL, gross_year REAL);
CREATE TABLE clients (id INTEGER PRIMARY KEY, user_id INTEGER, client_name TEXT, hours_worked REAL, amount_billed REAL, rate REAL);
```


### `app.py`
This is the main **routes** file for the app. For a better separation of concerns, I keep the logic on this file as minimal as possible. Instead of including the code for each functionality in this page, I returned a function for each POST request. These functions were imported from different files and organized by functionality. For instance, log in, log out and registering are handled in a file called `usermanagement.py` (more info below).

### `helpers.py`
This file includes the `login_required` decorator from Finance and two ad-hoc functions that are called from different files:
- `error`: loads an error page with an image and a personalized message.
- `validate_entry`: checks if a field form is empty and if it is an integer. As it returns 0 for empty fields, it avoids malfunctions if a user decides to leave a field empty. Also, it returns an error for non-integer inputs.

### `usermanagement.py`
This file handles the main functionalities related to user management: registering new users, logging users in and logging users out. The core code is similar to Finance, but I introduced some improvements:
- Instead of doing registration and login in just one big function, I tried to break down each one of them into its different components and write a different function for each of them. For instance, the register function calls **independent functions** to check if a user already exists, validate the password/confirmation and add the user to the database. This way, I hope my code will be easier to understand and more maintainable down the line.
- Error handling is done on the same page, rather than taking the user to a new one. That improves the user experience by reducing the number of clicks needed to complete the task in case an error happens.
- When a logged-in user visits the log in page, they see a message letting them know they are already logged in and linking them back to the homepage.
- Finally, I created two different homepages for logged in and logged out users.

### `ratecalculator.py`
This file handles the most complex functionality of this project: calculating a user’s minimum goal rate, taking into account a variety of factors.
From the point of view of the user experience, the Rate Calculator is divided into **4 different screens**. That way I avoided creating an overly long form that may detract from the usability of the website. Each screen has its own route:
- `/rate` handles the expenses section of the form. The user introduces information about long term, annual and monthly expenses. The program calculates the total annual expense and adds it to the database.
- `/rate2` handles the hours section of the form, where user introduces information about the time they expect to spend working. The program calculates the user’s billable time and billable hours per year and adds them to the database alongside the number of hours worked per day.
- `/rate3` handles the earnings section of the form, where the user introduces information about their salary expectations and applicable tax rate. The program calculates the gross earnings per year and the goal rate and adds them to the database, as well as the net salary per month and the tax rate.
- Finally, `/rate4` displays the result to the user, including the goal rate and the steps taken to calculate it.
This was the most complicated file of the project in terms of code optimization, since I was handling a lot of inputs and variables that are correlated between them. For a future version of this project, I would consider using classes to manage them more cleanly.

### `clienttool.py`
This file handles **Client tool** functionality, getting and validating inputs from the form and updating the database accordingly. If it is the first time the user introduces the client’s name, a new database entry is created. If it is an existing client, the database is updated. Finally, it also incorporates a function to delete clients.

### `summary.py`
This file checks existing information about a user.
If client information is available, it calls the `get_total_clients` function, that adds up information about all existing clients to obtain the user’s total hours worked, amount billed and average rate. If client and rate information is available, it calls the `get_message` function, that checks if current clients are above or below the goal rate and displays a message accordingly.
Finally, the information is sent to the `summary.html` template, which uses if/else logic to display different pages depending on the available data.

### `static` folder
The static folder contains an image for the error template and a CSS file. I mostly used **Bootstrap** components, so the standalone CSS is limited to small tweaks like fonts, text size/alignment and colors.

### `templates` folder
This folder contains **Jinja2** templates for the different pages on the site, all built on the same layout. Many of them contain personalized variables. I tried to keep the number of unique variables passed to each template as small as possible with the use of dictionaries.
Some templates, such as `login.html` and `register.html`, incorporate an integrated error variable that displays a personalized message in case something goes wrong. As discussed above, this makes possible to warn the user about mistakes without disrupting the navigation by taking them to a whole different page.

These templates incorporate a variety of Bootstrap elements for styling, including buttons, forms and a navigation bar.

## Ideas for version 2.0
I think version 1.0 of this program achieves its main goals, but of course there is a lot of room for improvement! Here are some ideas that I might consider incorporating into this project later on:
- Adding a projects table to the database to store information about each project independently and display it on My summary page below each client.
- Adding a script to the summary.html template so the user’s average rate turns green (if it is above goal rate) or red (if it is below goal rate).
- Adding functionality for updating clients.
- Improving the web design and front end for a more polished experience.
- Incorporating classes to the code and keep working on refactorization.
- Creating tests for each main feature.