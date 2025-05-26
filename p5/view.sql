---First, develop and test at least three views. Generate a script file called p5/view.sql with all of your view definitions 
---(with clear comments describing what the views represent and why it would be useful to your system - e.g. security, simplified querying, etc). 
---(Your views should have some complexity and cannot just be SELECT * FROM <table>).

---This is a view for department and all the salesperson that work for each department with their split info
---This view will be helpful for human resources and compensation calculation
DROP VIEW IF EXISTS v_dept_sa;
CREATE VIEW IF NOT EXISTS v_dept_sa 
AS 
    SELECT * FROM department NATURAL JOIN salesperson ORDER BY dept_id;

---This is a view for all the credit card payment information for each customer, along with the customer's email address and the card's payment address
---Only last 4 digits are shown for security purposes so this view can be used by all the salesperson and employees of the store to verify customer information
DROP VIEW IF EXISTS v_cc_info;
CREATE VIEW IF NOT EXISTS v_cc_info
AS 
    SELECT cc_belong_id, cust_id, card_id, cust_name, email_address, substr(card_number, -4) as cc_lastfour, 
    address_line1 || ' ' || CASE WHEN address_line2 IS NULL THEN '' ELSE address_line2 END || ' ' || town_city || ' ' || state_province || ' '|| country_area || ' ' || zip_code as full_address
    FROM cc_belong NATURAL JOIN customer NATURAL JOIN credit_card;


---This is a view that displays all the transaction details for the all the orders, including order date, item, quantity, price, customer and payment information
---This view is created using previously defined view - v_cc_info
DROP VIEW IF EXISTS v_order_detail;
CREATE VIEW IF NOT EXISTS v_order_detail
AS
    SELECT order_id, order_date, merch_name, order_quantity, msrp_price, cost_price, 
    cust_name, email_address as cust_email, cc_lastfour, full_address, sa_id 
    FROM orders NATURAL JOIN order_merch NATURAL JOIN merchandise NATURAL JOIN v_cc_info
    ORDER BY order_date asc, cust_name asc;


---This is a view that displays all the transaction details and the vendors for each order. This is important to help the store understand which vendor is the biggest partner
DROP VIEW IF EXISTS v_order_by_vendor;
CREATE VIEW IF NOT EXISTS v_order_by_vendor
AS
    SELECT order_id, merch_name, vendor_id 
    FROM (
        SELECT * 
        FROM orders 
        NATURAL JOIN order_merch)
    NATURAL JOIN merchandise;

