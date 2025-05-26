-- Develop and test at least four new SQL queries using the various constructs we have discussed in class_
-- and join at least three tables per query (with at least one of the tables having 10,000+ rows)._
-- At least two of your queries should involve aggregation._
-- To receive full credit, you should use at least two of the JOIN variations discussed in class (INNER, USING, NATURAL, OUTER).


--- 1. for salesperosn that have more than average salary, display the total number of transactions since 2021-10-01 that he/she achieved 
--- where the number of items bought exceeded the average quantity of items per transaction
--- 2 big + 1 small TABLE & LEFT OUTER JOIN & aggregation
SELECT sa_name, count(*) AS num_sales_since_oct21
FROM 
    (SELECT * 
    FROM orders
    LEFT OUTER JOIN order_merch USING (order_id) 
    LEFT OUTER JOIN salesperson USING (sa_id) 
    WHERE order_date > DATE('2021-10-01') 
        AND order_quantity > (SELECT avg(order_quantity) FROM order_merch) 
        AND salary > (SELECT avg(salary) FROM salesperson)
    ORDER BY order_date DESC)
GROUP BY sa_name;


--- 2. for each department display the salesperson with highest revenue, and calculate his/her total split from the revenue earned
--- 2 big table + 2 small table & natural join with aggregation
WITH dept_sa_rev AS (
    SELECT dept_name, sa_name, sum(order_revenue) AS total_revenue, sum(split_amt) AS total_split
    FROM 
        (
            SELECT *, order_quantity*msrp_price AS order_revenue, order_quantity*msrp_price*split AS split_amt 
            FROM orders 
            NATURAL JOIN order_merch 
            NATURAL JOIN merchandise 
            NATURAL JOIN department 
            NATURAL JOIN salesperson
        )
    GROUP BY dept_name, sa_name
    ORDER BY dept_name ASC, total_revenue ASC
)
SELECT * 
FROM dept_sa_rev
WHERE dept_sa_rev.sa_name IN (
    SELECT R.sa_name 
    FROM dept_sa_rev AS R 
    WHERE dept_sa_rev.dept_name = R.dept_name 
    ORDER BY total_revenue 
    DESC LIMIT 1
);



--- 3. displaying the customer in WA, AK, VT or TX states with first name that starts with A
--- 1 big + 2 small & inner join & natural join using
SELECT * 
FROM (
    SELECT * FROM customer WHERE cust_name LIKE 'A%'
    ) 
JOIN (
    SELECT * FROM cc_belong NATURAL JOIN credit_card WHERE state_province in ('WA', 'AK', 'VT', 'TX')
    ) 
USING (cust_id);



--- 4. for bulk orders (order_quantity between 40-50) that happend after 2021-01-01, display the frequency (number of times) that each order_quantity value appears
--- 2 big + 1 small & natural join & aggregation
SELECT order_quantity, count(*) AS frequency 
FROM (
    SELECT * FROM order_merch WHERE order_quantity BETWEEN 40 AND 50
    ) 
NATURAL JOIN (
    SELECT * FROM orders WHERE order_date > date('2021-01-01')
    ) 
NATURAL JOIN cc_belong 
GROUP BY order_quantity
ORDER BY order_quantity ASC;

