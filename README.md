# 100DaysofCode-Online-Shop
Day 97 of the 100 Days of Code course. For the day’s goal, the goal was to create a fully functional online shop. For this project, I used Flask with integration from Strip’s API to create the online shop.

In the screenshots folder, there are various screenshots for the shop’s pages and functionality. This includes screenshots for every page, as well as a screenshot of the payments received on Shop’s website.

The backofshop.py file takes care of email functionality for the website. When a customer submits the “contact us” form, an email is sent out with the information the user provided. Additionally, there is an email sent out when a customer walks through all the steps in the order check out process.

The feeders.py file is responsible for populating the products table in the online shop database. When initially testing to make sure that data was displayed properly on the Flask website, I was initially only working with the feeder insects (items) dictionary. After I was able to get the pages to render properly, that data was then passed to the onlineshop database which was then used to render information on the shop website. The feeders.py file is great for initiating the products table but if the table already exists, then the populate_product_table does not return anything.

The forms.py file is used to create all the forms used for the online shop. Forms include the contact form, login/register forms and shipping information form. Additionally, I created a Flask form for item quantity selection. Once the quantity is selected, the item is added to a customer’s cart.

Main.py ties everything together in initiating the database, rendering the web pages and managing all of the shop’s functionality. Additionally, within main.py the create-checkout-session route is used to redirect customers to a payment page. The payment page was created and tested using Stripe’s documentation and test card numbers to verify that payments would be submitted properly. Another resource that I found useful in successfully creating the Stipe payment page was referencing Testdriven.io’s tutorial in setting up the Stripe payment page. https://testdriven.io/blog/flask-stripe-tutorial/
