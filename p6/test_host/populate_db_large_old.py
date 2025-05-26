from re import L
from faker import Faker
import random
import csv

fake = Faker()
CNT_DEPT = 0
CNT_SA = 0
CNT_VENDOR = 0
CNT_SKU = 0
CNT_CC = 0
CNT_CUST = 0
CNT_CCBELONG = 0


SA_LST = []
SKU_LST = []
AVAIL_QTY_LST = []
CC_LST = []
CUST_NAME_LST = []

# 1. for populating the department table 
# very unlikely to have more than 10k departments in a store so kept the original size
DEPT_LST = [
    'Mens Shoes',
    'Womens Shoes',
    'Boys Shoes',
    'Girls Shoes',
    'Baby Shoes',
    'Mens Clothing',
    'Womens Clothing',
    'Boys Clothing',
    'Girls Clothing',
    'Baby Clothing',
    'Cosmetics',
    'Skincare',
    'Fragrance',
    'Gifts',
    'Books',
    'Toys',
    'Electronics',
    'Furniture',
    'Kitchen',
    'Bath',
    'Bed',
    'Decor']
CNT_DEPT = len(DEPT_LST) #22
with open('department.txt', 'w') as f:
    f.write("\n---for populating the deparment table\n")
    for i, dept in enumerate(DEPT_LST):
        # print("insert into department values (%s,'%s');" % (i,dept))
        f.write("insert into department values (%s,'%s');\n" % (i,dept))



# 2. for populating the salesperson entity
# expanding the salesperson table size to 11000
"""
create table salesperson(
    sa_id int primary key, 
	sa_name varchar(20) not null, 
	salary numeric(8,2) not null,
	dept_id int not null,
	split numeric(1,2) not null,
	foreign key (dept_id) references department)
"""
CNT_SA = 50
with open('salesperson.txt', 'w') as f:
    f.write("\n---for populating the salesperson table\n")
    for i in range(0, CNT_SA):
        name = fake.unique.name()
        while name in SA_LST:
            name = fake.unique.name()
        SA_LST.extend(name)
        salary = fake.pydecimal(left_digits=8, right_digits=2, positive=True, min_value=50000.00, max_value=200000.00)
        dept_id = random.randint(0, CNT_DEPT-1)
        split = fake.pydecimal(left_digits=2, right_digits=2, min_value=9, max_value=95)
        split = round(split/100,2)
        if split > 0.5: split = 1 - split
        # print("insert into salesperson values (%s,'%s', %s, %s, %s);" % (i, name, salary, dept_id, split))
        f.write("insert into salesperson values (%s,'%s', %s, %s, %s);\n" % (i, name, salary, dept_id, split))      



# 3. for populating the vendor table
# keeping the vendor table size
"""
create table vendor(
	vendor_id int primary key, 
	vendor_name varchar(50) not null);
"""
CNT_VENDOR = 20
with open('vendor.txt', 'w') as f:
    f.write("\n---for populating the vendor table\n")
    for i in range(0, CNT_VENDOR):
        vendor_name = fake.unique.company() 
        if not vendor_name.upper().endswith(('GROUP','LTD','LLC','INC','PLC')): 
            vendor_name += ' ' + fake.company_suffix()
        # print("insert into vendor values (%s,'%s');" % (i, vendor_name))
        f.write("insert into vendor values (%s,'%s');\n" % (i, vendor_name))


# 4. for populating the merchandise table
# keepint the merchandise table the same size
"""
create table merchandise(
	sku varchar(50) primary key,
	merch_name varchar(100) not null,
	msrp_price numeric(4,2) not null,
	inventory int not null,
	dept_id int not null, 
	vendor_id int not null,
	available_quantity int not null,
	cost_price numeric(4,2) not null,
	foreign key (dept_id) references department,
	foreign key (vendor_id) references vendor);
"""
MERCH_NAME_DEPT = [
    ('Tasman Slipper', 0), 
    ('Forum Mid Sneaker', 0),
    ('Cloud X Training Shoe', 0),
    ('Essentials Arizona Waterproof Slide Sandal', 1),
    ('Faux Fur Retro Hiking Sneaker', 1),
    ('Ultra Mini Boot', 1),
    ('Cloudswift Running Shoe', 1),
    ('Air Force 1 Sneaker', 2),
    ('Jefferson Water Friendly Slip-On Vegan Sneaker', 3),
    ('Free Run 2 Toddler Sneaker ', 4),
    ('Icon Bomber Jacket', 5),
    ('Hank Jogger Pants', 5),
    ('Wool Blend Beanie with Faux Fur Pom', 6),
    ('Future Icons Primegreen Logo Hoodie', 6),
    ('Kids Event21 Pullover Hoodie', 7),
    ('Kids Unicorn Sequin Glitter Dress', 8),
    ('Cristina Martinez Print Leggings', 8),
    ('Tutu Dress (Little Girl)', 9),
    ('Beautiful Skin Foundation', 10),
    ('Magic Cream Face Moisturizer with Hyaluronic Acid', 11),
    ('Kacey Musgraves Slow Burn Scented Candle', 12),
    ('Soft Lounge Robe', 13),
    ('Jungly Tails Cloth Book', 14),
    ('Younger Skin Starts in the Gut Book', 14),
    ('LEGO Creator 3-in-1 Safari Wildlife Tree House - 31116 ', 15),
    ('Disney x Ceaco 2-Pack 1000-Piece Puzzles', 15),
    ('True Evo Wireless Bluetooth Earbuds', 16),
    ('Packlite Chair', 17),
    ('Chunky Knit Sweater Handwoven Rug', 17),
    ('Comfort Roll Arm Slipcovered Sofa', 17),
    ('Mason Stoneware Canisters', 18),
    ('Hydrocotton Organic Quick-Dry Towels', 19),
    ('Belgian Flax Linen Waffle Duvet Cover', 20),
    ('Joshua Handcrafted Ceramic Vases', 21),
    ('Anton Desktop Clock', 21)
]
CNT_SKU = len(MERCH_NAME_DEPT) # 35
SKU_LST = []
AVAIL_QTY_LST = []
with open('merchandise.txt', 'w') as f:
    f.write("\n---for populating the merchandise table\n")
    for i in range(0, CNT_SKU):
        sku = fake.bothify(text='###????##', letters='abcdefghijklmnopqrstuvwxyz')
        while sku in SKU_LST: sku = fake.bothify(text='#####????', letters='abcdefghijklmnopqrstuvwxyz')
        SKU_LST.append(sku)

        merch_name = MERCH_NAME_DEPT[i][0]
        msrp_price = fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=9, max_value=420)
        # msrp_price = round( msrp_price/10, 2)
        inventory = fake.pyint(min_value=0, max_value=1000)
        dept_id = MERCH_NAME_DEPT[i][1]
        vendor_id = fake.pyint(min_value=0, max_value=20-1)
        available_quantity = random.randint(1, 1000)
        AVAIL_QTY_LST.append(available_quantity)
        discount = fake.pyfloat(left_digits=2, right_digits=2, min_value=0, max_value=10) / 10 
        if discount > 0.5: discount = 1 - discount
        cost_price = round(msrp_price * (1- discount), 2)
        # print("insert into merchandise values ('%s','%s', %s, %s, %s, %s, %s, %s);" % (sku, merch_name, msrp_price, inventory, dept_id, vendor_id, available_quantity, cost_price))
        f.write("insert into merchandise values ('%s','%s', %s, %s, %s, %s, %s, %s);\n" % (sku, merch_name, msrp_price, inventory, dept_id, vendor_id, available_quantity, cost_price))



# 5. for populating the credit_card table
# expand the size to 1500
"""
create table credit_card(
	card_id int primary key,
	card_number varchar(20) not null,
	address_line1 varchar(50) not null,
	address_line2 varchar(20),
	town_city varchar(50),
	state_province varchar(50) not null,
	country_area varchar(20) not null,
	zip_code varchar(20) not null);
"""
CNT_CC = 500
with open('credit_card.txt','w') as f:
    f.write("\n---for populating the credit_card table\n---expand the size to 1500\n")
    for i in range(0, CNT_CC):
        card_number = fake.unique.credit_card_number()
        while card_number in CC_LST: card_number = fake.unique.credit_card_number()
        CC_LST.append(card_number)

        addrs = fake.unique.address()
        while not ',' in addrs or 'APO' in addrs or 'FPO' in addrs.upper() or 'DPO' in addrs.upper() or 'PO' in addrs.upper() or 'BOX' in addrs.upper(): 
            addrs = fake.unique.address()

        addrs1, addrs2 = addrs.split('\n')
        addrs1 = addrs1.strip()
        addrs2 = addrs2.strip()
        city, state_zip = addrs2.split(', ')
        city = city.strip()
        sate_zip = state_zip.strip()
        state, zip = state_zip.split(' ')
        state = state.strip()
        zip = zip.strip()
        apts = [
            'APT.','Apt.', 'apt.', 
            'SUITE.', 'Suite.', 'suite.', 'STE.', 'Ste.', 'ste.',
            'UNIT.', 'Unit.', 'unit.',
            'APT', 'Apt', 'apt', 
            'SUITE', 'Suite', 'suite', 'STE', 'Ste', 'ste',
            'UNIT', 'Unit', 'unit']
        apt_in_addrs1 = [x in addrs1 for x in apts]
        if any(apt_in_addrs1):
            idx = apt_in_addrs1.index(True)
            street, apt = addrs1.split(apts[idx])
            street = street.strip()
            apt = apts[idx] + ' ' + apt.strip()
            # print("insert into credit_card values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (i, card_number, street, apt, city, state, "USA", zip))
            f.write("insert into credit_card values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');\n" % (i, card_number, street, apt, city, state, "USA", zip))
        else:
            street = addrs1
            # print("insert into credit_card values (%s, '%s', '%s', NULL, '%s', '%s', '%s', '%s');" % (i, card_number, street, city, state, "USA", zip))
            f.write("insert into credit_card values (%s, '%s', '%s', NULL, '%s', '%s', '%s', '%s');\n" % (i, card_number, street, city, state, "USA", zip))




# 6. for populating the customer table
"""
create table customer(
	cust_id int primary key,
	cust_name varchar(20) not null,
	email_address varchar(100),
	card_id int, 
	foreign key (card_id) references credit_card);
"""
cust_emails = []
CNT_CUST = 11200
with open('customer.txt', 'w') as f:
    f.write("\n---for populating the customer table\n---expanding to 11200\n")
    for i in range(0, CNT_CUST):
        cust_name = fake.unique.name()
        while cust_name in CUST_NAME_LST or cust_name in SA_LST:
            cust_name = fake.unique.name()
        CUST_NAME_LST.append(cust_name)

        cust_email = fake.unique.email()
        while cust_email in cust_emails or len(cust_email) > 100:
            cust_email = fake.unique.email()
        cust_emails.append(cust_email)
        # print("insert into customer values (%s, '%s', '%s');" % (i, cust_name, cust_email))
        f.write("insert into customer values (%s, '%s', '%s');\n" % (i, cust_name, cust_email))
        

# 7. for populating the cc_belong table
# expanding to size of the credit_card table which is 11500 (while the customer table is only 11200 so some customers will have more than one card)
"""
create table cc_belong(
	cc_belong_id int primary key,
	cust_id int not null,
	card_id int not null,
	foreign key (cust_id) references customer,
	foreign key (card_id) references credit_card);
"""
with open('cc_belong.txt', 'w') as f:
    f.write("\n---for populating the cc_belong table\n---expanding cc_belong table because of the expanded size of credit_card table\n")
    # for i in range(0, 1500): # we have CNT_CC = 1500 and CNT_CUST = 11200
    for i in range(0, CNT_CC): # we have CNT_CC = 1500 and CNT_CUST = 11200
        cust_id = random.randint(0, CNT_CUST-1)
        # cust_id = random.randint(0, 11200-1)
        card_id = i
        f.write("insert into cc_belong values (%s, %s, %s);\n" % (i, cust_id, card_id))
        # print("insert into cc_belong values (%s, %s, %s);" % (i, cust_id, card_id))
CNT_CCBELONG = CNT_CC
# CNT_CCBELONG = 1500


# 8. for populating the orders table
"""
create table orders(
	order_id int primary key,
	order_date datetime,
	cc_belong_id int not null,
	sa_id int, 0...24
	foreign key (cust_id) references customer,
	foreign key (card_id) references credit_card,
	foreign key (sa_id) references salesperson);
"""
# CNT_CCBELONG = 500
# CNT_SA = 50
CNT_ORDERS = 22000
with open('orders.txt', 'w') as f:
    f.write("\n---for populating the orders table\n---expanding the orders table to 25150\n")
    for i in range(0, CNT_ORDERS):
        order_date = fake.date_time_this_decade()
        # ccbelong_id = random.randint(0, 1500-1)
        ccbelong_id = random.randint(0, CNT_CCBELONG-1)
        if i % 11 == 0 or i % 3 == 0:
            sa_id = ''
            f.write("insert into orders values (%s, '%s', %s, NULL);\n" % (i, order_date, ccbelong_id))
        else:
            sa_id = random.randint(0, CNT_SA-1)
            # sa_id = random.randint(0, 11000-1)
            f.write("insert into orders values (%s, '%s', %s, %s);\n" % (i, order_date, ccbelong_id, sa_id))



# 9. for populating the order_merch table
"""
create table order_merch(
	order_id int,
	sku int,
	order_quantity int not null,
	primary key (order_id, sku),
	foreign key (order_id) references orders,
	foreign key (sku) references merchandise);
"""

CNT_ORDER_MERCH = 0
with open('order_merch.txt', 'w') as f:
    f.write("\n---for populating the order_merch table\n---expanding the order_merch table as orders table expanded, goal is to make it bigger than 50,000\n")
    # for i in range(0, 25150-1):
    for i in range(0, CNT_ORDERS-1):
        num = random.randint(1, 4)
        CNT_ORDER_MERCH += num
        sku_ordered = []
        while num > 0:
            idx = random.randint(0, CNT_SKU-1)
            # idx = random.randint(0, 35-1)
            sku = SKU_LST[idx]
            while sku in sku_ordered: # so that we for one order_id (i), we don't have a sku appear multiple times
                idx = random.randint(0, CNT_SKU-1)
                # idx = random.randint(0, 35-1)
                sku = SKU_LST[idx]
            sku_ordered.append(sku)
            qty = random.randint(1, max(round(AVAIL_QTY_LST[idx]/20,0), 2))
            f.write("insert into order_merch values (%s, '%s', %s);\n" % (i, sku, qty))
            # print("insert into order_merch values (%s, '%s', %s);" % (i, sku, qty))
            num -= 1
    
    # The last order
    i = CNT_ORDERS
    idx = random.randint(0, CNT_SKU-1)
    # idx = random.randint(0, 35-1)
    sku = SKU_LST[idx]
    qty = random.randint(1, max(round(AVAIL_QTY_LST[idx]/20,0), 2))
    f.write("insert into order_merch values (%s, '%s', %s);\n" % (i, sku, qty))



# 10. 11. 12 for populating the in_cart, favorite, review tables
"""
create table in_cart(
	cust_id int,
	sku varchar(50),
	cart_quantity int not null,
	primary key (cust_id, sku),
	foreign key (cust_id) references customer,
	foreign key (sku) references merchandise);

create table favorite(
	cust_id int,
	sku varchar(50),
	primary key (cust_id, sku),
	foreign key (cust_id) references customer,
	foreign key (sku) references merchandise);

create table review(
	cust_id int,
	sku varchar(50),
	star int not null,
	primary key (cust_id, sku),
	foreign key (cust_id) references customer,
	foreign key (sku) references merchandise);
"""

cnt = 150
cust_lst = []
with open('in_cart.txt', 'w') as f:
    f.write("\n---for populating the in_cart table\n")
    while cnt > 0: # the length of customers list
        i = random.randint(0, CNT_CUST-1)
        while i in cust_lst: 
            i = random.randint(0, CNT_CUST-1)
        cust_lst.append(i)

        num = random.randint(1, 3)
        sku_incart = []
        while num > 0:
            idx = random.randint(0, CNT_SKU-1)
            sku = SKU_LST[idx]
            while sku in sku_incart: # so that we for one order_id (i), we don't have a sku appear multiple times
                idx = random.randint(0, CNT_SKU-1)
                sku = SKU_LST[idx]
            sku_incart.append(sku)
            
            qty = random.randrange(1, max(round(AVAIL_QTY_LST[idx]/20,0), 2))
            f.write("insert into in_cart values (%s, '%s', %s);\n" % (i, sku, qty))
            # print("insert into in_cart values (%s, '%s', %s);" % (i, sku, qty))
            num -= 1
        cnt -= 1

cnt = 5200
cust_lst = []
with open('favorite.txt', 'w') as f:
    f.write("\n---for populating the favorite table\n---expanding the size\n")
    while cnt > 0:
        i = random.randint(0, CNT_CUST-1)
        while i in cust_lst: 
            i = random.randint(0, CNT_CUST-1)
        cust_lst.append(i)

        num = random.randint(1, 3)
        sku_favorite = []
        while num > 0:
            idx = random.randint(0, CNT_SKU-1)
            sku = SKU_LST[idx]
            while sku in sku_favorite: # so that we for one order_id (i), we don't have a sku appear multiple times
                idx = random.randint(0, CNT_SKU-1)
                sku = SKU_LST[idx]
            sku_favorite.append(sku)
            f.write("insert into favorite values (%s, '%s');\n" % (i, sku))
            # print("insert into favorite values (%s, '%s');" % (i, sku))
            num -= 1
        cnt -= 1


cnt = 120
cust_lst = []
with open('review.txt', 'w') as f:
    f.write("\n---for populating the review table\n")
    while cnt > 0:
        i = random.randint(0, CNT_CUST-1)
        while i in cust_lst: 
            i = random.randint(0, CNT_CUST-1)
        cust_lst.append(i)

        num = random.randint(1, 2)
        sku_review = []
        while num > 0:
            idx = random.randint(0, CNT_SKU-1)
            sku = SKU_LST[idx]
            while sku in sku_review: # so that we for one order_id (i), we don't have a sku appear multiple times
                idx = random.randint(0, CNT_SKU-1)
                sku = SKU_LST[idx]
            sku_review.append(sku)
            star = random.randint(1, 10)
            star = star/2
            f.write("insert into review values (%s, '%s', %s);\n" % (i, sku, star))
            # print("insert into review values (%s, '%s', %s);" % (i, sku, star))
            num -= 1
        cnt -= 1