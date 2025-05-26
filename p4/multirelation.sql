---Develop and test at least five multi relation SQL queries (queries involving multiple tables). 
---At least two of these should include a subquery. Generate a script file called multirelation.sql with all of your queries.


---list all the salesperson for departments that sell men's stuff
with dept_mens as (select dept_name from department where dept_name like '%Men%' or dept_name like '%men%' except select dept_name from department where dept_name like '%Women%' or dept_name like '%women%')
select * from dept_mens natural join salesperson;

--shows the customers that have their favorite skus in their shopping cart now
with fav_in_cart (cust_id, sku) as (select in_cart.cust_id, in_cart.sku from in_cart join favorite on in_cart.cust_id = favorite.cust_id and in_cart.sku = favorite.sku) select * from fav_in_cart;


--- shows the full details of each cutomer and their credit card
select * from customer left join cc_belong on customer.cust_id = cc_belong.cust_id left join credit_card on cc_belong.card_id = credit_card.card_id;


---shows the details of each order that's place after 2021-01-10, with merchandise name, price, quantity, order_date and customer name
select order_id, order_quantity, merch_name, msrp_price, order_date, cust_name from (select * from orders where order_date > date('2021-01-10 00:00:00')) natural join order_merch natural join merchandise natural join cc_belong natural join customer order by order_id;

---shows the in_cart details of each customer with the merchandise name listed
select * from customer join in_cart on customer.cust_id = in_cart.cust_id left join merchandise on in_cart.sku = merchandise.sku;


--show the orders that do not a salesperson associated and their payment & customer information
select * from (select * from orders where orders.sa_id is NULL) natural join cc_belong natural join customer;

