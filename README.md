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
### Setup
The project first imports the necessary modules and components from the files listed above. The program also has constants and environment variables that are set up at the top of the main.py file.
With that, the Flask application and database are set up for this project. The database used is a SQLite database and has three tables.
-	Products: Contains the store products.
-	User: Contains site user data.
-	Cart: Contains the user’s carts, which combines data from the products and user tables.
If the database file is brand new, the products table gets populated with the data that is loaded from the feeders.py file.
### Flask Routes
#### Home Route
This route returns the splash page when someone visits the website. On this page, the user is presented with the option to enter the store.
#### Shop Home
The **Shop Home** route displays the website’s online catalog of items that are available for sale. Each card displays an item image, name, price, rating, and an option to view an individual item.

On the website's navbar, only the shop home route is presented. This route does not redirect to the splash page.
#### Selected Product
The **selected product** route displays an individual item when a user selects it from the home page.

The page itself pulls data from the products database table and presents a user with the following:
-	Item image, name, rating, description, and item price.
-	A drop-down allowing users to add items to the user’s cart. Additionally, the user is informed that they must log in to add an item to their cart.

Once a user adds an item to their cart, they are redirected to their shopping cart, which reflects the new items added, and if a value is updated, the new value is reflected.
#### Login
The **login** route allows a user to log into the website. If the data entered does not match the database entry, they are informed that the account may not exist or that their password is incorrect. If a user successfully logs in, they are redirected to the shop home page.
#### Register
The **register** page allows users to register for an account on the website. If an account already exists, they are redirected to the login page.
#### Logout
This route logs out a user who is currently logged in.
#### Cart
The **cart** route returns the user’s shopping cart. This route is only accessible if a user is logged in and pulls data from the shopping cart table.

On the page itself, the user is presented with the items they have added to their cart, the item’s price, quantity, and an option to remove the item. The cart's subtotal is also displayed. 
Additionally, there are options to continue shopping or proceed to the shipping page.
#### Update Item
The update route redirects the user to the selected products page, allowing them to update the item’s quantity.
#### Remove Item
If the user clicks on the remove link in their shopping cart, this route removes the item from their cart. This change is also reflected in the database.
#### Shipping
The **shipping** page displays the **ShippingForm**, which the user populates with their shipping information.

Once the form is submitted, the global **SHIPPING_ADDRESS constant** is updated to reflect the data that is provided by the user.  The user then proceeds to the payment page.
#### Payment
The **payment information** page is the next step in the checkout process. This page displays the user’s order details, shipping and contact information, and the option to proceed to process a payment. Payments processed on this website are completed utilizing Stripe and are initiated in the following route.
#### Create Checkout Session
The **create checkout session** route redirects the user to the Stripe payment page. Payments on this website were processed using Stripe’s test mode as a proof of concept to make sure that payments could be processed successfully. 

If a payment is successful, the user is directed to the order confirmation page. If a payment is canceled, they are returned to the shipping page. 

*To create a checkout session, a Stripe API key is needed*.
#### Order Confirmation
The **order confirmation** page is the last step in the checkout process. Once a user’s order is processed, they are redirected to this page. If the cart is empty, or the user tries to access the page with no shipping address information, they are redirected to the appropriate step in the checkout process.

If an order is successful, the global constants are reset, and the user is sent an email containing their order details. Additionally, the database is updated to reflect that the checkout process has been completed. 
#### Contact
The **contact** page contains a contact form that can be submitted by site visitors.

This page contains the **ContactForm**, and when a **POST request** is submitted, the data passed by the user is sent to the site administrator using smtplib.
#### Message Delivered
When a visitor submits a message, they are redirected to a page informing them that their message has been delivered.
#### About
**About** provides information about the online store. Text for this page was generated with Gen AI.
#### FAQ
**FAQ** provides FAQ information about the online store. Text for this page was generated with Gen AI.


## Project Flowcharts
Insert flowcharts
## Project Screenshots
Screenshots for this project can be found in the [screenshots folder](/screenshots).
