
select *
from 
    (select count(*) as cnt_dept from department),
    (select count(*) as cnt_sa from salesperson),
    (select count(*) as cnt_vendor from vendor),
    (select count(*) as cnt_merch from merchandise),
    (select count(*) as cnt_customer from customer),
    (select count(*) as cnt_cc from credit_card),
    (select count(*) as cnt_cc_belong from cc_belong),
    (select count(*) as cnt_orders from orders),
    (select count(*) as cnt_order_merch from order_merch),
    (select count(*) as cnt_in_cart from in_cart),
    (select count(*) as cnt_favorite from favorite),
    (select count(*) as cnt_review from review);