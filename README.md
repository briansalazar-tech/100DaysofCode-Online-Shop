# 100 Days of Code Day 97: Online Shop 
![Splash page screenshot](<screenshots/splash page.png>)

**Table of Contents**
1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [Modules Used](#modules-used)
4. [Project Files](#project-files)
5. [Project Walkthrough](#project-walkthrough)
6. [Project Flowcharts](#project-flowcharts)
7. [Project Screenshots](#project-screenshots)
## Introduction
This repo contains the code for my attempt at the day 97 portfolio project of the 100 Days of Code course. For the day’s goal, the goal was to create a fully functional online shop. For this project, I used Flask with integration from Stripe’s API to create the online shop.

Of all the projects completed in the course, this one was the most time-intensive and thorough in fleshing out. The only aspect missing was inventory tracking capabilities; however, that leaves the door open for future improvements.
In the [screenshots folder](/screenshots), there are various screenshots for the shop’s pages and functionality. This includes screenshots for every page, as well as a screenshot of the payments received on Stripe’s website.
## Technologies Used
### Stripe API
To create a fully functional online shop, a payment processing platform had to be used. In this project, [**Stripe**](https://www.stripe.com) is used to process payments. Since the project is a personal project and not a production website, payments were processed in “test mode”. 

To integrate the Stripe API, [Stripe’s documentation](https://docs.stripe.com/api) was referenced. In addition, the following tutorial from [testdriven.io](https://testdriven.io/blog/flask-stripe-tutorial/) was very useful in setting up payment processing.
## Modules Used
### Os & Dotenv
The **os** and **dotenv** modules are used in the project to load environment variables.
### Pandas
**Pandas** is used to render data from the database onto the web page being accessed. This includes rendering the website’s inventory and retrieving the user’s cart. 
### Stripe
To use the **Stripe API**, the **Stripe** module must be imported.
### Random
**Random’s** functionality for this project is aesthetic in purpose. When a user’s order is completed, a randomized order number is generated. This helps achieve a more realistic feel when completing an order instead of starting off from order number 00001. 
### Flask & Flask Bootstrap
**Flask** and **Flask-Bootstrap** are needed in this project to render the various routes used for the website as well as templating and displaying the web pages correctly.
### Flask Forms
**Flask Forms** is used to create the various forms used in this project. The table below highlights the forms used on this website:

| Form | Form Overview |
| :------------------- | :------------------- |
| Contact form         | The contact form is submitted by visitors to contact the website’s administrators.      |
| Login form           | This form is rendered on the login page and allows users to login.      |
| Register form        | This form is rendered on the register page and allows users to create an account.      |
| Shipping form        | This form is accessed on the shipping page of the checkout process.      |
| Quantity selection   | The quantity selection form is used as a simple dropdown that allows customers to select the quantity of items they would like to order.      |

### Flask SQLAlchemy
This project utilizes a SQLite database to keep track of persistent data. To interact with the onlineshop.db file, **SQLAlchemy** is used. This includes creating the database if it does not exist, updating, adding items, and deleting items from the database. 
### Flask Login
**Flask Login** is used to manage user logins. This includes logging users in, logging them out, and getting the details for the currently logged in user.
### Werkzeug
**Werkzeug** is used to create hashed passwords when a user creates an account on the website. Additionally, the module checks that the hash is correct when someone tries to login after creating an account.
### Functools
The **wraps function** from **Funnctools** is used to redirect the user to a 403 page when they attempt to access a resource that requires authentication. 
### Smtplib
**Smtplib** is used to send emails when a contact form response is submitted or when a user’s order is completed.
### Email
There were some formatting issues when sending emails using only smtplib to compose the email’s body. To work around this, the **EmailMessage class** was used to compose the body of the email that gets sent.
### Datetime
The **datetime** module is used in the backofshop.py file to get the current date and save it to a variable. The date is important as it is used for payment confirmation and whenever someone submits a response on the contact page.
## Project Files
### Onlineshop.db
The **onlineshop.db** file is the relational database file used for this project. The database file has three tables:
-	**Products**: The Products table keeps track of all of the online shops' products. If the database is brand new, the populate_product_table function is used to populate the table with the data from the feeders.py file. 
-	**User**: The Users table is used to keep track of users who have registered an account.
-	**Shopping** Cart: This table is composed of the items in a user’s cart. When an order is updated or completed, those changes are reflected in this table.
### Static folder
The static folder contains the website images, CSS styling, as well as the **JavaScript code needed to process payments**.
### Templates folder
The templates folder contains all the HTML template files used for the online shop project.
### Backofshop.py
The **backofshop.py** file takes care of email functionality for the website.

When a customer submits the “contact us” form, an email is sent out with the information the user provided. 

Additionally, an email is sent when a customer walks through all the steps in the order checkout process.
### Feeders.py
The **feeders.py** file is responsible for populating the products table in the online shop database. 

*When initially testing to ensure the data was displayed properly on the Flask website, I was initially only working with the feeder insects (items) dictionary. After I was able to render the pages properly, that data was then passed to the onlineshop database, which was then used to render information on the shop website. The feeders.py file initiates the products table, but if the table already exists, then the populate_product_table does not return anything.*
### Forms.py
The **forms.py** file is used to create all the forms used for the online shop. Forms include the contact form, login/register forms, and shipping information form. Additionally, I created a Flask form for item quantity selection. Once the quantity is selected, the item is added to a customer’s cart.
### Main.py
**Main.py** ties everything together in initiating the database, rendering the web pages, and managing all the shop’s functionality. 

Additionally, within main.py the **create-checkout-session route** is used to redirect customers to a payment page. The **payment page** was created and tested using Stripe’s documentation and test card numbers to verify that payments would be submitted properly. 

The **Project Walkthrough** section will provide more details on the functionality of main.py.
## Project Walkthrough
Insert walkthrough
## Project Flowcharts
Insert flowcharts
## Project Screenshots
Screenshots for this project can be found in the [screenshots folder](/screenshots).
