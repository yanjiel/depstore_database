Database Requirement
The database that dept_store_server.py interacts with - webserverdata.db - is supplied here. 

This .db can also be replicated by running p3/drop_tables.sql, p3/create_db.sql, p3/populate_db.sql and save as webserverdata.db. 

This database has the same schema and desgin as my project, which can be seen in p2/description.txt and p2/schema.txt

Execution of Python File
Just python3 dept_store_server.py and then launch http://localhost:8080/listall in browser


Flow of Web Server
1. http://localhost:8080/listall will display a list of all salespersons in the salesperson table

2. at the end of each salesperson row, there is a delete link that will direct the user to http://localhost:8080/delete/sa_id,  which will execute the query to delete salesperson with that particual sa_id to be deleted from the salesperson table

3. at the bottom of the /listall page, there is a form for new salesperson information. After hitting submit, users will be directly to http://localhost:8080/insert and that new salsperson will be inserted into the salesperson table. *More work will be needed to make sure the user submit values that are in the domain boundary or meet integrity checks

4. finally revisiting/refreshing http://localhost:8080/listall will always give the user the most up-to-date list of salespersons in the salesperson table