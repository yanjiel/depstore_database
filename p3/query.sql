
-- ---shows salesperson list and the department name that they work for
-- select * from salesperson natural join department;

-- ---shows the number of salesperson, their average salary and average split for each deparment of the store
-- select dept_name, count(*) as num_of_sa, avg(split), avg(split) from salesperson natural join department group by dept_name;

-- ---shows the number of salesperson departments that sell men's stuff
-- select dept_name, count(*) as num_of_sa from salesperson natural join department where dept_name like 'Mens%' group by dept_name;

-- ---shows the number of orders each salesperson has assisted with
-- select count(*) as num_of_orders, sa_name from orders natural join salesperson group by sa_name;

-- --- shows the full details of each cutomer and their credit card
-- select * from customer left join cc_belong on customer.cust_id = cc_belong.cust_id left join credit_card on cc_belong.card_id = credit_card.card_id;

-- ---shows the details of each order, with merchandise name, price, quantity, order_date and customer name
-- select order_id, order_quantity, merch_name, msrp_price, order_date, cust_name from order_merch natural join merchandise natural join orders natural join customer order by order_id;

-- ---shows the number of oders and total revenue (msrp_price * order_quantity in orders table) for each department
-- select dept_name, count(*) as num_of_orders, sum(order_quantity*msrp_price) as total_revenue from order_merch natural join merchandise natural join department group by dept_name;

-- ---shows the in_cart details of each customer with the merchandise name listed
-- select * from customer join in_cart on customer.cust_id = in_cart.cust_id  left join merchandise on in_cart.sku = merchandise.sku;

-- -- shows the details of each customer's favorite merchandise
-- select * from favorite natural join customer;

-- --- find the average star/review for each sku, and many customers have reviewd on it
-- select sku, avg(star), count(star) from review natural join customer group by sku;


--show the departments in the store that sell Men's stuff
select * from department where dept_name like 'Mens%';

--show all the salesperson that work for department number 7 which is Boys Clothing
select * from salesperson where dept_id = 7;

--show the total number of orders salesperson number 19 has assisted with
select * from orders where sa_id = 19;

--show the order details of orders that do not a salesperson associated
select * from orders where sa_id is NULL;

--show number of orders that do not a salesperson associated
select count(*) from orders where sa_id is NULL;

--show the number of distince skus that have been bought vs the toal number of orders that have been placed
select count(distinct(sku)) as num_of_distinct_sku, count(*) as num_of_orders from order_merch;

--show the highest to lowest price merchandise
select * from merchandise order by msrp_price desc;

--show the top 10 merchandise with highest margins (unit profit)
select merch_name,  (msrp_price - cost_price) as margin from merchandise order by margin desc limit 10;

--show the merchandise reviewed by highest average review (star) first
select * from review order by star desc;

--sort the reviews by customer acending and star descending
select * from review order by cust_id asc, star desc;

--show the cart items that a customer have more than 9 of them in their cart, with sku sorted ascending and cart_quantity sorted descending
select cust_id, sku, cart_quantity from in_cart where cart_quantity > 9 order by sku asc, cart_quantity desc;
