---Next, develop and test at least six SQL queries using the JOIN syntax discussed in class 
---(up to three of these can be modified versions of your multirelation queries from last week, and should be labeled as such). !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
---Generate a script file called p5/query.sql with all of your queries. 
---This set of queries should meet the below requirements:
---At least two of these queries should involve aggregation (both queries should include the GROUP BY clause and at least one query should include a HAVING clause).
-- Each of your views should be referenced in at least one query.
-- At least one of the queries should use a temporary table. The temp table declaration must appear in the query.sql file.
-- You must use at least three of the four JOIN variations discussed in class (ON, USING, NATURAL, OUTER).
-- Your queries must not produce empty results.
-- There should be at least one CASE statement.


--- list customer with all their cards' last 4 digit, if not a credit card on file then display "NOT FOUND"
--- used OUTER JOIN, USING, CASE
WITH cust_cc_all AS (
    SELECT * 
    FROM (
        SELECT * 
        FROM customer 
        LEFT OUTER JOIN cc_belong 
        USING (cust_id)
        ) 
    LEFT OUTER JOIN credit_card 
    USING (card_id)
)
SELECT cust_name, CASE WHEN card_id IS NULL THEN 'NOT FOUND' ELSE substr(card_number, -4) END AS cc_lastfour 
FROM cust_cc_all
ORDER BY cust_name, cc_lastfour;




--- find the favorite list for the customers that do not have credit cards on file
--- used OUTER JOIN, NATURAL JOIN, ON, VIEW (v_cc_info), TEMPORARY TABLE
DROP TABLE IF EXISTS temp_fav_merch;
CREATE TEMP TABLE IF NOT EXISTS temp_fav_merch AS 
    SELECT cust_id, sku, merch_name, msrp_price, available_quantity, vendor_name 
    FROM favorite NATURAL JOIN merchandise NATURAL JOIN vendor;

WITH cust_no_card AS (SELECT cust_id, cust_name FROM customer WHERE cust_id NOT IN (SELECT cust_id FROM v_cc_info)) 
SELECT cust_no_card.cust_id, cust_name AS cust_name_no_card, merch_name AS favorite_merch, msrp_price, available_quantity, vendor_name 
FROM cust_no_card 
LEFT OUTER JOIN temp_fav_merch 
ON cust_no_card.cust_id = temp_fav_merch.cust_id;



--- find the number of unsold skus (skus that have not appeared in any order) by department, and the total inventory of all unsold skus for that department - only if
--- the deparment's total (unsold) inventory is greater than the average total inventory of all departments
--- used NATURAL JOIN, GROUP BY HAVING, VIEW (v_order_detail)
WITH 
    merch_dept AS (
        select * 
        from merchandise 
        natural join department 
        order by dept_name asc, merch_name asc
        )
SELECT dept_name, count(sku) AS num_unsold_skus, sum(inventory) AS total_remaining_inventory 
FROM merch_dept
WHERE merch_name NOT IN (SELECT merch_name FROM v_order_detail) 
GROUP BY dept_name
HAVING total_remaining_inventory > (SELECT avg(totalinv) from (SELECT sum(inventory) as totalinv from merch_dept as R group by R.dept_id));




--- find the most achieving salesperson for each department, judged by his/her total revenue achieved in that department, and calculate his/her split for all transactions
--- used GROUP BY, LEFT JOIN, USING, TEMP table, VIEW (v_dept_Sa)
DROP TABLE IF EXISTS temp_dept_sa_revenue;
CREATE TEMP TABLE IF NOT EXISTS temp_dept_sa_revenue AS 
    SELECT order_id, order_date, merch_name, order_quantity*msrp_price AS order_revenue, dept_name, sa_name, salary, split 
    FROM v_order_detail NATURAL JOIN v_dept_sa;

WITH rev_by_dept_sa AS (
    SELECT dept_name, sa_name, sum(order_revenue) AS total_revenue
    FROM temp_dept_sa_revenue 
    GROUP BY dept_name, sa_name 
    ORDER BY dept_name ASC, total_revenue ASC
)
SELECT dept_name, sa_name, total_revenue, total_revenue*split AS split_amt 
FROM (
    SELECT * 
    FROM rev_by_dept_sa AS L 
    WHERE L.sa_name IN (
        SELECT R.sa_name 
        FROM rev_by_dept_sa AS R 
        WHERE L.dept_name = R.dept_name 
        ORDER BY total_revenue 
        DESC LIMIT 1)
)
LEFT JOIN salesperson
USING (sa_name);




--- find the top 3 MOST popular vendor judged by number of orders sold that has merchandises from that vendor
WITH order_vendor AS (
    SELECT order_id, merch_name, vendor_name 
    FROM v_order_by_vendor
    LEFT JOIN vendor 
    USING (vendor_id)
)
SELECT vendor_name, count(*) AS num_of_orders 
FROM order_vendor 
GROUP BY vendor_name 
ORDER BY num_of_orders DESC 
LIMIT 3;


--- filter the reviews on merchandise by each customer, to include the reviews on merchandises that a customer has bought
--- uses NATURAL JOIN
WITH 
    sku_order AS (
        SELECT cust_id, sku 
        FROM (
            SELECT cc_belong_id, sku 
            FROM orders 
            NATURAL JOIN order_merch) 
        NATURAL JOIN cc_belong
        ORDER BY cust_id ASC, sku ASC
    )
SELECT cust_name, merch_name AS merch_bought_reviewed, star
FROM (
    SELECT * 
    FROM (
        SELECT distinct cust_id, sku, star
        FROM review  
        WHERE sku IN (
            SELECT sku 
            FROM sku_order
            WHERE review.cust_id = sku_order.cust_id)
    )
    NATURAL JOIN customer
)  
NATURAL JOIN merchandise;



