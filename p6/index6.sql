--- this will help the third query in query6.sql where we filtering customer table by customer name (cust_name)
--- for query 3 in query6.sql, before creating index, the Run Time: real 0.046 user 0.000000 sys 0.000000
--- for query 3 in query6.sql, after creating index, the Run Time: real 0.015 user 0.000000 sys 0.000000
CREATE INDEX IF NOT EXISTS cust_name_idx ON customer (cust_name);


--- this will help the first and fourth query in query6.sql where we filtering orders table by order_date
--- for query 4 in query6.sql, before creating index, the Run Time: real 0.105 user 0.015625 sys 0.000000
--- for query 4 in query6.sql, after creating index, the Run Time: real 0.079 user 0.015625 sys 0.046875
CREATE INDEX IF NOT EXISTS order_date_idx ON orders (order_date);


--- this will help the first and fourth query in query6.sql where we filtering order_merch table by order_quantity
--- for query 4 in query6.sql, before creating index, the Run Time: real 0.105 user 0.015625 sys 0.000000
--- for query 4 in query6.sql, after creating index, the Run Time: real 0.008 user 0.000000 sys 0.000000 
CREATE INDEX IF NOT EXISTS order_qty_idx ON order_merch (order_quantity);