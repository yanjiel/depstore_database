---Develop and test at least two SQL schema modifications (one of each type - ADD column, DROP column). 
---Generate a script file called schemamodification.sql with all of your schema modifications (note that one of not too many functionalities that sqlite does not support is ALTER column https://www.sqlite.org/omitted.html)

---add column in credit card entity to show the full complete payment address
ALTER TABLE credit_card ADD COLUMN address_line varchar(70);

---drop the column from credit card
ALTER TABLE credit_card DROP COLUMN address_line;


--add column in merchandise to show the per unit margin of a sku that can be calculated from attributes mrsp_price - attribute cost_price
ALTER TABLE merchandise ADD COLUMN margin numeric(5,2);

--drop the column from merchandise
ALTER TABLE merchandise DROP COLUMN margin;



