---Develop and test at least two of the four types of SQL data modification commands (for a total of eight commands): 
---INSERT a single tuple, INSERT using an output control (insert using select), DELETE and UPDATE. 
---Generate a script file called modification.sql with all of your data modifications.

---insert a new customer Alexcito Gondalez
INSERT INTO customer VALUES (23, 'Alexcito Gondalez', 'agondaliez@gmail.com');

---insert a new vendor
INSERT INTO vendor VALUES (20, 'BMW of North America LLC');

-- ---insert a transaction: new order entry since a customer just placed a new order with the help of a salesperson, and the order is 1 of sku 126nwns31
-- BEGIN TRANSACTION;
-- INSERT INTO order_merch VALUES(30, '126nwns31', 1);
-- INSERT INTO orders VAlUES (30, '2022-02-05 14:10:00', 18, 1);
-- COMMIT;

---insert using output control
--add to favorite list the skus that are bought
INSERT INTO favorite 
SELECT * FROM (
    WITH order_sku AS (select cust_id, sku, cust_id || '-' || sku as uniq_id from orders natural join cc_belong natural join order_merch), fav_sku AS (select *, cust_id || '-' || sku as uniq_id from favorite)
    SELECT distinct cust_id, sku FROM order_sku WHERE uniq_id NOT IN (select uniq_id from fav_sku)
);

--add to in_cart list the skus that are favorite
INSERT INTO in_cart 
SELECT * FROM (
    WITH fav_sku AS (select *, cust_id || '-' || sku as uniq_id from favorite), cart_sku AS (select cust_id, sku, cust_id || '-' || sku as uniq_id from in_cart) 
    SELECT distinct cust_id, sku, 1 FROM fav_sku WHERE uniq_id NOT IN (select uniq_id from cart_sku)
);
    
---add a new salesperson to the department where we have fewest salesperson, lowest average salary
INSERT INTO salesperson
SELECT 25, 'John Doe', avg_salary, dept_id, avg_split FROM
(
    SELECT dept_id, avg(salary) as avg_salary, avg(split) as avg_split from department natural join salesperson group by dept_id order by count(*) asc, avg(salary) asc limit 1
);


---delete the new customer Alexcito Gondalez
DELETE FROM customer WHERE cust_name = 'Alexcito Gondalez';

---delete orders placed on or after date 2022-02-05
DELETE FROM orders WHERE order_date >= '2022-02-05 00:00:00';



---update customer email
UPDATE customer SET email_address = 'gmartinez@gmail.com' WHERE cust_name = 'Glen Martinez';

---I've actually made a mistake by placing zipcodes in country_area column and country_area in zip_code column so I am swapping them by using update command
UPDATE credit_card SET country_area = zip_code, zip_code = country_area;

