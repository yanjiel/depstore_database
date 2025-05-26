**Database Requirement**
1. The database that dept_store_server.py interacts with - webserverdata.db - is supplied here. 

2. This .db can also be re-created by running p3/drop_tables.sql, p3/create_db.sql, p3/populate_db.sql and save as webserverdata.db in the same folder as the dept_store_server.py file

3. This database has the same schema and desgin as my project, which can be seen in p2/description.txt and p2/schema.txt

**Execution of Python File**
Just python3 dept_store_server.py and then launch http://localhost:8080/homepage in browser


**Flow of Web Server**
1. http://localhost:8080/homepage will display a form where user can fill in searching criteria for an order in the orders table (relationX). After filling the search criteria (or leave blank to retrieve the top 30 orders result) and click on "Search", user will be directed to http://localhost:8080/search_order

2. http://localhost:8080/search_order at the top there is a form to add a new order, followed by a table showing search results that meet the search criteria filled in homepage in step above. Each row of result is an entry in the orders table, detailing the order_id, order_date, customer, credit_card and salesperson info for that particular order (attributes relationX), followed by these functions:

	a View/Edit link that directs user to http://localhost:8080/edit_order/order_id, which will allow users to update attribute values of that particular order_id in the orders table(relationX)

	a Delete link that directs user to http://localhost:8080/delete_order/order_id, which will allow user to delete that particular order_id entry from the orders table  (relationX)

	a Show Merchandise link that directs user to http://localhost:8080/show_ordermerch/order_id, which will join query from order_merch table (relationY) and display the merchandise & their quantities (attributes of relationY) for that particular order_id

	a Add Merchandise link that directs to http://localhost:8080/add_ordermerch/order_id, which allow users to insert entries into order_merch table (relationY) for that particular order_id

