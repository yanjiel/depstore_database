---Develop and test at least three SQL queries involving aggregation. Generate a script file called aggregation.sql with all of your queries.

---shows the number of salesperson, their average salary and average split for each deparment of the store
select dept_name, count(*) as num_of_sa, avg(split), avg(split) from salesperson natural join department group by dept_name;

---shows the number of oders and total revenue (msrp_price * order_quantity in orders table) for each department
select dept_name, count(*) as num_of_orders, sum(order_quantity*msrp_price) as total_revenue from order_merch natural join merchandise natural join department group by dept_name;

--- find the average star/review for each sku, and many customers have reviewd on it
select sku, avg(star), count(star) from review natural join customer group by sku;

---shows the number of orders each salesperson has assisted with
select count(*) as num_of_orders, sa_name from orders natural join salesperson group by sa_name;