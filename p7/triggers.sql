-- Write at least three triggers (put your trigger definitions in a script called triggers.sql). 
-- Add a comment before each trigger describing what the trigger should do.
-- One of your triggers should enforce an integrity constraint on your database, this could be a complex attribute constraint/
-- check or it could be a constraint that needs to check the state of another table(s) to ensure the state of the DB is 'correct'.
-- One trigger should keep track of changes to a given table in a log table (if you do not already have a log table in your database
-- - which is very likely - you should create one for this assignment). Add a create table statement, and write/insert record changes
-- to this log to capture how data changes in your create_db.sql file. Such a log table is meant to record changes to some other table in the DB. 
-- You do not need to capture all data from the change, but capture at least one attribute that was changed 
-- (for example I log changes to the user's email address).
-- One trigger can do anything you want it to do! 
-- For a complete reference of the trigger syntax, read https://www.sqlite.org/lang_createtrigger.html




--- trigger 1.a before inserting a new order_merch entry, make sure that the order_quantity is smaller than the available_quantity, if not abort
create trigger order_quantity_check_1 before insert on order_merch
for each row
when 
    new.order_quantity > (select available_quantity from merchandise where merchandise.sku = new.sku)
begin
    select raise(abort, 'order quantity exceeds available quantity');
end;
--- trigger 1.b when available_quantity check is met then continue with the order_merch insert and update available quantity
create trigger order_quantity_check_2 after insert on order_merch
for each row
when 
    new.order_quantity <= (select available_quantity from merchandise where merchandise.sku = new.sku)
begin
    update merchandise set available_quantity = available_quantity - new.order_quantity where merchandise.sku = new.sku;
end;





--- trigger 2. keep track of changes to customer email
CREATE TABLE IF NOT EXISTS cust_email_change (
    cust_id int not null,
    change_date datetime not null,
    old_email varchar(100),
    primary key (cust_id, change_date)
    foreign key (cust_id) references customer
);
create trigger cust_email_change after update of email_address on customer
begin
    insert into cust_email_change values (old.cust_id, CURRENT_TIMESTAMP, old.email_address);
end;




--- trigger 3. on deleting a salesperson or updating a dept_id of a salesperson, make sure that it does not leave any departments with 0 salesperson under it
--- however the overall state of the department table is maintained by an integrity constraint that's placed on the database itself
create trigger sa_headcount_check before update of dept_id on salesperson
for each row
when 
    (select count(*) from salesperson where dept_id = old.dept_id) <= 1
begin
    select raise(abort, 'departments cannot have less than 1 salesperson');
end;
