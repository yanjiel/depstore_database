from re import L
from faker import Faker
import random

fake = Faker()

# for populating the department table
dept_lst = [
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
print("\n---for populating the deparment table")
for i, dept in enumerate(dept_lst):
    print("insert into department values (%s,'%s');" % (i,dept))


# for populating the salesperson entity
"""
create table salesperson(
    sa_id int primary key, 
	sa_name varchar(20) not null, 
	salary numeric(8,2) not null,
	dept_id int not null,
	split numeric(1,2) not null,
	foreign key (dept_id) references department)
"""
sa_dept_lst=[
    (0, 7),
    (1, 5),
    (2, 11),
    (3, 19),
    (4, 2),
    (5, 6),
    (6, 13),
    (7, 13),
    (8, 7),
    (9, 18),
    (10, 1),
    (11, 8),
    (12, 21),
    (13, 15),
    (14, 7),
    (15, 12),
    (16, 9),
    (17, 0),
    (18, 10),
    (19, 14),
    (20, 17),
    (21, 4),
    (22, 20),
    (23, 16),
    (24, 3)
]
sa_names=[]
print("\n---for populating the salesperson table")
for i in range(0,25):
    name = fake.unique.name()
    while name in sa_names:
        name = fake.unique.name()
    sa_names.extend(name)
    salary = fake.pydecimal(left_digits=8, right_digits=2, positive=True, min_value=50000.00, max_value=200000.00)
    #dept_id = fake.pyint(min_value=0, max_value=len(dept_lst)-1)
    dept_id = sa_dept_lst[i][1]
    split = fake.pydecimal(left_digits=2, right_digits=2, min_value=9, max_value=95)
    split = round(split/100,2)
    if split > 0.5: split = 1 - split
    print("insert into salesperson values (%s,'%s', %s, %s, %s);" % (i, name, salary, dept_id, split))


# for populating the vendor table
"""
create table vendor(
	vendor_id int primary key, 
	vendor_name varchar(50) not null);
"""
print("\n---for populating the vendor table")
for i in range(0,20):
    vendor_name = fake.unique.company() 
    if not vendor_name.upper().endswith(('GROUP','LTD','LLC','INC','PLC')): 
        vendor_name += ' ' + fake.company_suffix()
    print("insert into vendor values (%s,'%s');" % (i, vendor_name))


#for populating the merchandise table
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
merch_name_dept = [
    ('Tasman Slipper', 1), 
    ('Forum Mid Sneaker', 1),
    ('Cloud X Training Shoe', 1),
    ('Essentials Arizona Waterproof Slide Sandal', 2),
    ('Faux Fur Retro Hiking Sneaker', 2),
    ('Ultra Mini Boot', 2),
    ('Cloudswift Running Shoe', 2),
    ('Air Force 1 Sneaker', 3),
    ('Jefferson Water Friendly Slip-On Vegan Sneaker', 4),
    ('Free Run 2 Toddler Sneaker ', 5),
    ('Icon Bomber Jacket', 6),
    ('Hank Jogger Pants', 6),
    ('Wool Blend Beanie with Faux Fur Pom', 7),
    ('Future Icons Primegreen Logo Hoodie', 7),
    ('Kids Event21 Pullover Hoodie', 8),
    ('Kids Unicorn Sequin Glitter Dress', 9),
    ('Cristina Martinez Print Leggings', 9),
    ('Tutu Dress (Little Girl)', 10),
    ('Beautiful Skin Foundation', 11),
    ('Magic Cream Face Moisturizer with Hyaluronic Acid', 12),
    ('Kacey Musgraves Slow Burn Scented Candle', 13),
    ('Soft Lounge Robe', 14),
    ('Jungly Tails Cloth Book', 15),
    ('Younger Skin Starts in the Gut Book', 15),
    ('LEGO Creator 3-in-1 Safari Wildlife Tree House - 31116 ', 16),
    ('Disney x Ceaco 2-Pack 1000-Piece Puzzles', 16),
    ('True Evo Wireless Bluetooth Earbuds', 17),
    ('Packlite Chair', 18),
    ('Chunky Knit Sweater Handwoven Rug', 18),
    ('Comfort Roll Arm Slipcovered Sofa', 18),
    ('Mason Stoneware Canisters', 19),
    ('Hydrocotton Organic Quick-Dry Towels', 20),
    ('Belgian Flax Linen Waffle Duvet Cover', 21),
    ('Joshua Handcrafted Ceramic Vases', 22),
    ('Anton Desktop Clock', 22)
]
sku_lst = []
avail_qty_lst = []
print("\n---for populating the merchandise table")
for i in range(0,len(merch_name_dept)):
    sku = fake.bothify(text='###????##', letters='abcdefghijklmnopqrstuvwxyz')
    while sku in sku_lst: sku = fake.bothify(text='#####????', letters='abcdefghijklmnopqrstuvwxyz')
    sku_lst.append(sku)
    merch_name = merch_name_dept[i][0]
    msrp_price = fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=9, max_value=420)
    # msrp_price = round( msrp_price/10, 2)
    inventory = fake.pyint(min_value=0, max_value=1000)
    dept_id = merch_name_dept[i][1]
    vendor_id = fake.pyint(min_value=0, max_value=20-1)
    available_quantity = random.randrange(0, 1000)
    avail_qty_lst.append(available_quantity)
    discount = fake.pyfloat(left_digits=2, right_digits=2, min_value=0, max_value=10) / 10 
    if discount > 0.5: discount = 1 - discount
    cost_price = round(msrp_price * (1- discount), 2)
    print("insert into merchandise values ('%s','%s', %s, %s, %s, %s, %s, %s);" % (sku, merch_name, msrp_price, inventory, dept_id, vendor_id, available_quantity, cost_price))


# for populating the credit_card table
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
print("\n---for populating the credit_card table")
for i in range(0,22):
    card_number = fake.unique.credit_card_number()
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
        print("insert into credit_card values (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (i, card_number, street, apt, city, state, zip, "USA"))
    else:
        street = addrs1
        print("insert into credit_card values (%s, '%s', '%s', NULL, '%s', '%s', '%s', '%s');" % (i, card_number, street, city, state, zip, "USA"))


# for populating the customer table
"""
create table customer(
	cust_id int primary key,
	cust_name varchar(20) not null,
	email_address varchar(100),
	card_id int, 
	foreign key (card_id) references credit_card);
"""
# cust_card_lst = [
#     (0, 1),
#     (1, 10),
#     (2, 9),
#     (3, 16),
#     (4, 8),
#     (5, 12),
#     (6, 2),
#     (7, 3),
#     (8, 7),
#     (9, 20),
#     (10, 11),
#     (11, 19),
#     (12, ''),
#     (13, 4),
#     (14, 6),
#     (15, 5),
#     (16, 0),
#     (17, 13),
#     (18, 14),
#     (19, 15),
#     (20, 17),
#     (21, 18),
#     (22, 21)
#     ]
cust_names = []
cust_emails = []
print("\n---for populating the customer table")
for i in range(0, 23):
    cust_name = fake.unique.name()
    while cust_name in cust_names or cust_name in sa_names:
        cust_name = fake.unique.name()
    cust_names.append(cust_name)
    cust_email = fake.unique.email()
    while cust_email in cust_emails or len(cust_email) > 100:
        cust_email = fake.unique.email()
    cust_emails.append(cust_email)
    
    # card_id = cust_card_lst[i][1]
    # if card_id != '' :
    #     print("insert into customer values (%s, '%s', '%s', %s);" % (i, cust_name, cust_email, card_id))
    # else:
    #     print("insert into customer values (%s, '%s', '%s', NULL);" % (i, cust_name, cust_email))
    
    print("insert into customer values (%s, '%s', '%s');" % (i, cust_name, cust_email))

# for populating the cc_belong table
"""
create table cc_belong(
	cc_belong_id int primary key,
	cust_id int not null,
	card_id int not null,
	foreign key (cust_id) references customer,
	foreign key (card_id) references credit_card);
"""
ccbelong_lst = [
    (0, 1, 10),
    (1, 2, 9),
    (2, 3, 16),
    (3, 4, 18),
    (4, 5, 12),
    (5, 6, 2),
    (6, 7, 3),
    (7, 8, 7),
    (8, 9, 20),
    (9, 10, 11),
    (10, 11, 19),
    (11, 13, 1),
    (12, 13, 4),
    (13, 14, 6),
    (14, 15, 5),
    (15, 16, 0),
    (16, 17, 13),
    (17, 18, 14),
    (18, 19, 15),
    (19, 20, 17),
    (20, 21, 18),
    (21, 22, 21)
]
print("\n---for populating the cc_belong table")
for i in range(0, len(ccbelong_lst)):
    cust_id = ccbelong_lst[i][1]
    card_id = ccbelong_lst[i][2]
    print("insert into cc_belong values (%s, %s, %s);" % (i, cust_id, card_id))


# for populating the orders table
"""
create table orders(
	order_id int primary key,
	order_date datetime,
	cust_id int not null,
	card_id int not null,
	sa_id int, 0...24
	foreign key (cust_id) references customer,
	foreign key (card_id) references credit_card,
	foreign key (sa_id) references salesperson);
"""
order_ccbelong_sa_lst = [
    (0, 3, 24),
    (1, 8, 0),
    (2, 21, ''),
    (3, 16, 19),
    (4, 17, 19),
    (5, 18, 10),
    (6, 2, ''),
    (7, 2, 5),
    (8, 15, 5),
    (9, 15, ''),
    (10, 3, 6),
    (11, 6, 6),
    (12, 4, 20),
    (13, 1, 11),
    (14, 6, 6),
    (15, 6, 6),
    (16, 6, 6),
    (17, 8, 1),
    (18, 8, 2),
    (19, 8, 9),
    (20, 8, 8),
    (21, 7, 4),
    (22, 0, ''),
    (23, 12, 0),
    (24, 10, 0),
    (25, 14, 15),
    (26, 9, 15),
    (27, 13, 16),
    (28, 13, 17),
    (29, 12, 18)
]

print("\n---for populating the orders table")
for i in range(0, len(order_ccbelong_sa_lst)):
    order_date = fake.date_time_this_decade()
    ccbelong_id = order_ccbelong_sa_lst[i][1]
    sa_id = order_ccbelong_sa_lst[i][2]
    if sa_id != '':
        print("insert into orders values (%s, '%s', %s, %s);" % (i, order_date, ccbelong_id, sa_id))
    else:
        print("insert into orders values (%s, '%s', %s, NULL);" % (i, order_date, ccbelong_id))


# for populating the order_merch table
"""
create table order_merch(
	order_id int,
	sku int,
	order_quantity int not null,
	primary key (order_id, sku),
	foreign key (order_id) references orders,
	foreign key (sku) references merchandise);
"""
print("\n---for populating the order_merch table")
for i in range(0,  len(order_ccbelong_sa_lst)):
    num = random.randrange(1,5)
    sku_ordered = []
    while num > 0:
        idx = random.randrange(0, len(sku_lst))
        sku = sku_lst[idx]
        while sku in sku_ordered: # so that we for one order_id (i), we don't have a sku appear multiple times
            idx = random.randrange(0, len(sku_lst))
            sku = sku_lst[idx]
        sku_ordered.append(sku)
        qty = random.randrange(1, max(round(avail_qty_lst[idx]/20,0), 2))
        print("insert into order_merch values (%s, '%s', %s);" % (i, sku, qty))
        num -= 1


# for populating the in_cart, favorite, review tables
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

print("\n---for populating the in_cart table")
for i in range(0,  23): # the length of customers list
    if i in [0, 8, 22]:
        # randomly pick three customers to have empty carts
        continue
    num = random.randrange(1,5)
    sku_incart = []
    while num > 0:
        idx = random.randrange(0, len(sku_lst))
        sku = sku_lst[idx]
        while sku in sku_incart: # so that we for one order_id (i), we don't have a sku appear multiple times
            idx = random.randrange(0, len(sku_lst))
            sku = sku_lst[idx]
        sku_incart.append(sku)
        qty = random.randrange(1, max(round(avail_qty_lst[idx]/20,0), 2))
        print("insert into in_cart values (%s, '%s', %s);" % (i, sku, qty))
        num -= 1

print("\n---for populating the favorite table")
for i in range(0,  23): # the length of customers list
    if i in [0, 6, 10, 15]:
        # randomly pick three customers to have empty carts
        continue
    num = random.randrange(1,5)
    sku_favorite = []
    while num > 0:
        idx = random.randrange(0, len(sku_lst))
        sku = sku_lst[idx]
        while sku in sku_favorite: # so that we for one order_id (i), we don't have a sku appear multiple times
            idx = random.randrange(0, len(sku_favorite))
            sku = sku_lst[idx]
        sku_favorite.append(sku)
        print("insert into favorite values (%s, '%s');" % (i, sku))
        num -= 1


print("\n---for populating the review table")
for i in range(0,  23): # the length of customers list
    if i in [0, 3, 8, 22]:
        # randomly pick three customers to have empty carts
        continue
    num = random.randrange(1,5)
    sku_review = []
    while num > 0:
        idx = random.randrange(0, len(sku_lst))
        sku = sku_lst[idx]
        while sku in sku_review: # so that we for one order_id (i), we don't have a sku appear multiple times
            idx = random.randrange(0, len(sku_review))
            sku = sku_lst[idx]
        sku_review.append(sku)
        star = random.randrange(0, 10)
        star = star/2
        print("insert into review values (%s, '%s', %s);" % (i, sku, star))
        num -= 1