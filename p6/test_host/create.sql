DROP TABLE IF EXISTS host;
CREATE TABLE host(
    hid int primary key,
    name varchar(20),
    age int
);
.import 'C:\Users\Adele Liu\Documents\GitHub\project-yanjiel\p6\copy\host.csv' host

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    order_id int primary key,
    order_date datetime,
    cc_belong_id int not null
);
.import 'C:\Users\Adele Liu\Documents\GitHub\project-yanjiel\p6\copy\orders.csv' orders

