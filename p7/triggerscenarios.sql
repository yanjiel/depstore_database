-- To show that your triggers work create a script called triggerscenarios.sql that shows, for each trigger, the effect of two database modifications. 
-- One modification should activate the trigger while the other should not. 
-- In the script, show queries that demonstrate that the trigger has an effect in the first case and not in the second one. 
-- (To be clear: you are creating three triggers and two modifications per trigger, for a total of six modifications, along with six queries
--- showing the results of the modifications. Be sure to add comments explaining the expected outcome of each modification and query.) 
-- The queries for showing the outcome of the trigger can be (and likely should be) very simple.


--- triggerscenario for trigger 1 (on the insert of entry (order_id, sku, quantity) into the order_merch table)
--- This will activate trigger 1.a but will not activate trigger 1.b since the order quantity will be greater than the available quantity (17)
--- you will first see the beginning available quantity for this sku, then an error raised and an empty result for the last query since the new order of that quantity did not go through
select available_quantity as available_quantity_before_order from merchandise where sku = '242kgta74';
INSERT INTO order_merch values (29, '242kgta74', 50);
select * from order_merch natural join merchandise where order_id = 29 and sku = '242kgta74';

--- This will not activate trigger 1.a but will activate trigger 1.b since the order quantity is less than the available quantity (17)
--- you will first see the beginning available quantity for this sku, then an entry for this order_merch with an updated available_quantity
select available_quantity as available_quantity_before_order from merchandise where sku = '242kgta74';
INSERT INTO order_merch values (29, '242kgta74', 10);
select * from order_merch natural join merchandise where order_id = 29 and sku = '242kgta74';




--- triggerscenario for trigger 2 (a change-logging trigger placed on updating attribute emaill_address of customer table)
--- This will not activate trigger 2 because it's not an update on the right attribute
UPDATE customer SET cust_name = 'Glen Martinez II' WHERE cust_id = 4;
select * from customer natural join cust_email_change where cust_id = 4;

--- This will activate trigger 2, which will insert a new entry into the cust_email_change table detailing the time of the email change and the old email_address that's being changed
UPDATE customer SET email_address = 'gmartinez@gmail.com' WHERE cust_id = 4;
select * from customer natural join cust_email_change where cust_id = 4;





--- triggerscenario for trigger 3 (on the update of dept_id attribute of the salesperson table)
--- This will activate trigger 3 since salesperson with sa_id = 17 was assigned to dept_id 0, which had no other salespersons; 
--- so re-assigning him/her to dept_id 8 DID not pass the check, therefore two queries will show the SAME department headcounts before and afte the udpate
select dept_id, count(*) as old_num_sa from salesperson group by dept_id order by dept_id;
UPDATE salesperson SET dept_id = 8 WHERE sa_id = 17;
select dept_id, count(*) as new_num_sa from salesperson group by dept_id order by dept_id;

--- This will not activate trigger 3 since salesperson with sa_id = 14 was assigned to dept_id 7, which had two more salespersons beside him/her; 
--- so re-assigning him/her to dept_id 8 passed the check, therefore two queries will show the DIFFERING department headcounts before and afte the udpate
select dept_id, count(*) as old_num_sa from salesperson group by dept_id order by dept_id;
UPDATE salesperson SET dept_id = 8 WHERE sa_id = 14;
select dept_id, count(*) as new_num_sa from salesperson group by dept_id order by dept_id;


