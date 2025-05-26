# select order_id, order_date, cust_id, cust_name, card_id, card_number from orders natural join cc_belong natural join customer natural join credit_card;
# select cc_belong_id, cust_id, cust_name, card_id, card_number from cc_belong natural join customer natural join credit_card;

########search by date
########auto add customer, auto add credit card
from bottle import route, run, template, post, get, request
import sqlite3
from datetime import datetime

con = sqlite3.connect('webserverdata.db')
cur = con.cursor()

@route('/homepage')
def hello():
    html = "<h2> Search for Order History </h2> <br />"

    html += '''
        <form action = "/search_order" method = "post">
            Order ID: <input name = "order_id" type="text" />
            Order Date(yyyy-mm-dd): <input name = "order_date" type="text" />
            Customer(*): <input name = "cust_name" type="text" />
            CC Last 4: <input name = "cc_last4" type="text" />
            Salesperson(*): <input name = "sa_name" type="text" />
            <input value = "Search Order" type = "submit" />
        </form>
    '''
    return html



@post('/search_order')
def search():
    order_id = request.forms.get('order_id').strip()
    order_date = request.forms.get('order_date').strip()
    cust_name = request.forms.get('cust_name').strip()
    cc_last4 = request.forms.get('cc_last4').strip()
    sa_name = request.forms.get('sa_name').strip()
    
    sql = 'select order_id, order_date, cust_name, card_number, sa_name from orders natural join cc_belong natural join customer natural join credit_card left outer join salesperson using (sa_id)'
    where_lst = []
    if not order_id and not order_date and not cust_name and not cc_last4 and not sa_name:
        sql += ' order by order_id desc limit 30'
    else:
        sql += ' where '
        if order_id:
            try: order_id = int(order_id)
            except: return "Invalid Order ID, integer expected </br> Return to <a href = \"/homepage\">main page</a>"
            else: where_lst.append("order_id = " + str(order_id))
        if order_date:
            try: order_date = datetime.strptime(order_date, "%Y-%m-%d")
            except: return "Invalid Order Date input, 'YYYY-mm-dd' format expected </br> Return to <a href = \"/homepage\">main page</a>"
            else: where_lst.append("DATE(order_date) = DATE('" + datetime.strftime(order_date, '%Y-%m-%d')+ "')")
        if cust_name:
            where_lst.append("cust_name like '%" + cust_name + "%'")
        if cc_last4:
            # try: cc_last4=int(cc_last4)
            # except: return "Invalid CC Last 4 Digit input, integer expected </br> Return to <a href = \"/homepage\">main page</a>"
            # else: where_lst.append['substr(card_number, -4) = '+ str(cc_last4)]
            where_lst.append("substr(card_number, -4) = '" + str(cc_last4) + "'")
        if sa_name:
            where_lst.append("sa_name like '%" + sa_name + "%'")
        sql += ' and '.join(where_lst)
        sql += ' order by order_id desc limit 30' # make sure the latest on top

    print(sql)
    html = "<h2> Order Search Result </h2> <br />"
    html += "<a href = \"/homepage\">Back to Search</a> <br /><br /><br />"
    html += "<h3> Order(s) Found</h3>"
    html += "<table> <tr> <td> order_id </td> <td> order_date </td> <td> cust_name </td> <td> card_number </td> <td> salesperson </td>    </tr>"
    for row in cur.execute(sql):
        html += "<tr>"
        for cell in row[0:5]:
            html += "<td>" + str(cell) + "</td>"
        # cc_belong_id = row[5]
        # sa_id = row[6]
        ########################################
        html += "<td><a href=\"/edit_order/" + str(row[0]) + "\">View / Edit</a> </td> "
        html += "<td><a href=\"/delete_order/" + str(row[0]) + "\">Delete</a> </td> "
        html += "<td><a href=\"/show_ordermerch/" + str(row[0]) + "\">Show Merchandise</a> </td> "
        html += "<td><a href=\"/add_ordermerch/" + str(row[0]) + "\">Add Merchandise</a> </td>  </tr>"
    html += "</table>"

    html += "<br /><br /><br /><br /><br />"
    html += "<h3> Add a New Order </h3>"
    html += '''
        <form action = "/insert_order" method = "post">
            Order Date (yyyy-mm-dd hh:mm:ss): <input name = "order_date" type="text" />
            Customer Name: <input name = "cust_name" type="text" />
            Credit Card Number: <input name = "card_number" type="text" />
            Salesperson(optional): <input name = "sa_name" type="text" />
            <input value = "Add Order" type = "submit" />
        </form>
    '''
    html += "*Please note, customer and credit card relationship will be check against cc_belong table to ensure no customer can use other customer's credit card </br>"
    html += "<i>*Sample customer name and credit card number combination: </br> &emsp; Glen Martinez 4091783370278452 </br > &emsp; Melinda Todd 503860971814 </br> &emsp; Melinda Todd 5590820425632920 </i>"
    return html



@post('/insert_order')
def insert_order():
    order_date = request.forms.get('order_date').strip()
    cust_name = request.forms.get('cust_name').strip()
    card_number = request.forms.get('card_number').strip()
    sa_name = request.forms.get('sa_name').strip()
    print(order_date, cust_name, card_number, sa_name)

    # validate order_date
    try: order_date = datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S")
    except: return "Error inserting new order. Expected Order Date format: %Y-%m-%d %H:%M:%S </br> Return to <a href = \"/homepage\">main page</a>"
    # validate cust_name and locate cust_id
    if not cust_name:
        return "Error inserting new order. Customer field cannot be blank </br> Return to <a href = \"/homepage\">main page</a>"
    else: 
        cur.execute("select cust_id from customer where cust_name = '" + cust_name + "'")
        try: cust_id = cur.fetchone()[0]
        except: "Error inserting new order. Customer not in system </br> Return to <a href = \"/homepage\">main page</a>"
            
    # validate card_number and locate card_id
    if not card_number:
        return "Error inserting new order. Credit Card field cannot be blank </br> Return to <a href = \"/homepage\">main page</a>"
    else: 
        cur.execute("select card_id from credit_card where card_number = '" + card_number + "'")
        try: card_id = cur.fetchone()[0]
        except: return "Error inserting new order. Credit Card not in system </br> Return to <a href = \"/homepage\">main page</a>"

    # validate sa name and locate sa
    if not sa_name:
        sa_id = None
    else:
        cur.execute("select sa_id from salesperson where sa_name = '" + sa_name + "'")
        try: sa_id = cur.fetchone()[0]
        except: return "Error inserting new order. Salesperson " + sa_name + " not in system. Leave blank or enter valid a Salesperson name </br> Return to <a href = \"/homepage\">main page</a>"
        
    # validate the card_number belongs to the customer
    # if no cc_belong info is found for this card, then add a new cc_belong entry
    # if cc_belong info is found for this card but registered under a different customer name, then reject the order entry
    cur.execute("select cc_belong_id from cc_belong where card_id = " + str(card_id) + " and cust_id = " + str(cust_id))
    try: 
        cc_belong_id = cur.fetchone()[0]
    except:
        cur.execute("select cc_belong_id from cc_belong where card_id = " + str(card_id))
        if cur.fetchone() is not None:
            return "Error inserting new order. Credit card " + str(card_number)[-4:] + " does not belong to customer " + cust_name + "</br> Return to <a href = \"/homepage\">main page</a>"
        else:
            # Then we add a cc_belong record id
            cur.execute("select max(cc_belong_id) from cc_belong")
            cc_belong_id = cur.fetchone()[0]
            cur.execute("insert into cc_belong values ({0}, {1}, {2})".format(cc_belong_id, cust_id, card_id))
            con.commit()
        
    # if pass integrity checks then add the new order with a new unique order_id
    cur.execute("select max(order_id) from orders")
    order_id = cur.fetchone()[0] + 1

    if sa_id is not None:
        print("insert into orders values ({0}, '{1}', {2}, {3})".format(order_id, datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S"), cc_belong_id, sa_id))
        cur.execute("insert into orders values ({0}, '{1}', {2}, {3})".format(order_id, datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S"), cc_belong_id, sa_id))
        con.commit()
    else:
        print("insert into orders values ({0}, '{1}', {2}, NULL)".format(order_id, datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S"), cc_belong_id))
        cur.execute("insert into orders values ({0}, '{1}', {2}, NULL)".format(order_id, datetime.strftime(order_date, "%Y-%m-%d %H:%M:%S"), cc_belong_id))
        con.commit()

    return "New order {} inserted </br> Return to <a href = \"/homepage\">main page</a> </br> Continue to <a href = \"/edit_order/{}\">View/Edit Order</a>".format(order_id, order_id)




@route('/delete_order/<order_id>')
def delete(order_id):
    cur.execute("delete from orders where order_id = '" + str(order_id) + "'")
    cur.execute("delete from order_merch where order_id = '" + str(order_id) + "'") # to preserver the foreign key constraint
    con.commit()
    return "order_id " + order_id + " deleted </br> Return to <a href = \"/homepage\">main page</a>"




@route('/edit_order/<order_id>')
def view_edit(order_id):
    
    html = "<h2> Order View / Edit</h2> <br />"
    html += "<a href = \"/homepage\">Back to Search</a> <br />"
    html += "<a href = \"/show_ordermerch/{}\">Show Order Merchandise</a> <br />".format(order_id)
    html += "<a href = \"/add_ordermerch/{}\">Add Order Merchandise</a> <br />".format(order_id)
    html += "<a href = \"/delete_order/{}\">Delete Order</a> <br /><br /><br />".format(order_id)

    html += "<h3> Order Details for order_id {} </h3>".format(order_id)
    html += "<table> <tr> <td> order_id </td> <td> order_date </td> <td> cust_name </td> <td> card_number </td> <td> salesperson </td>    </tr>"
    sql = 'select order_id, order_date, cust_name, card_number, sa_name from orders natural join cc_belong natural join customer natural join credit_card left outer join salesperson using (sa_id) where order_id = {}'.format(order_id)
    for row in cur.execute(sql):
        html += "<tr>"
        for cell in row[0:5]:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"

    html += "<br /><br /><br /><br /><br />"
    html += "<h3> Edit Details for order_id {} </h3>".format(order_id)
    html += '''
        <form action = "/update_order/{}" method = "post">
            Order Date (yyyy-mm-dd hh:mm:ss): <input name = "order_date" type="text" />
            Customer Name: <input name = "cust_name" type="text" />
            Credit Card Number: <input name = "card_number" type="text" />
            Salesperson(optional): <input name = "sa_name" type="text" />
            <input value = "Update Order" type = "submit" />
        </form>
    '''.format(order_id)

    html += "*Blank fields are not updated. </br>*Please note, customer and credit card relationship will be check against cc_belong table after update to ensure no customer can use other customer's credit card </br>"
    html += "<i>*Sample customer name and credit card number combination: </br> &emsp; Glen Martinez 4091783370278452 </br > &emsp; Melinda Todd 503860971814 </br> &emsp; Melinda Todd 5590820425632920 </i>"
    return html


@post('/update_order/<order_id>')
def update_order(order_id):
    order_date_new = request.forms.get('order_date').strip()
    cust_name_new = request.forms.get('cust_name').strip()
    card_number_new = request.forms.get('card_number').strip()
    sa_name_new = request.forms.get('sa_name').strip()
    #print(order_date_new, cust_name_new, card_number_new, sa_name_new)

    if not order_date_new and not cust_name_new and not card_number_new and not sa_name_new:
        return "Order_id {} not updated. </br> Return to <a href = \"/edit_order/{}\">View/Edit Page</a>".format(order_id, order_id)

    sql = 'update orders set '
    update_lst = []
    # validate order_date
    if order_date_new:
        try: order_date_new = datetime.strptime(order_date_new, "%Y-%m-%d %H:%M:%S")
        except: return "Error updating order_id {}. Expected Order Date format: %Y-%m-%d %H:%M:%S </br> Return to <a href = \"/edit_order/{}\">View/Edit Page</a>".format(order_id, order_id)
        else: update_lst.append("order_date = DATETIME('{}')".format(datetime.strftime(order_date_new, "%Y-%m-%d %H:%M:%S")))

    if not cust_name_new:
        cur.execute("select cust_name from orders natural join cc_belong natural join customer where order_id = {}".format(order_id))
        cust_name_new = cur.fetchone()[0] # keep new cust_name the same as the old cust_name
    if not card_number_new:
        cur.execute("select card_number from orders natural join cc_belong natural join credit_card where order_id = {}".format(order_id))
        card_number_new = cur.fetchone()[0] # keep new card_number the same as the old card_number
    # print(cust_name_new, card_number_new)

    # see if cust_name_new owns card_number_new, if does we can safely update
    # if not, see if card_number_new belongs to anyone else
    # if it's a new card then add to credit_card and then update cc_belong
    cur.execute("select cc_belong_id from cc_belong natural join customer natural join credit_card where cust_name = '{}' and card_number = '{}'".format(cust_name_new, card_number_new))
    # print("select cc_belong_id from cc_belong natural join customer natural join credit_card where cust_name = '{}' and card_number = '{}'".format(cust_name_new, card_number_new))
    try:
        cc_belong_id_new = cur.fetchone()[0]
    except:
        cur.execute("select cc_belong_id from cc_belong natural join credit_card where card_number = '{}'".format(card_number_new))
        # print("select cc_belong_id from cc_belong natural join credit_card where card_number = '{}'".format(card_number_new))
        if cur.fetchone() is not None: # means this is an existing card that belongs to someone else
            return "Error updating order_id {}. Updated credit card belongs to some other customer </br> Return to <a href = \"/edit_order/{}\">View/Edit Page</a>".format(order_id, order_id)
        else: # means this is a new card and we need to add the card to the credit_card table
            cur.execute("select max(card_id) from credit_card")
            card_id_new = cur.fetchone()[0] + 1
            cur.execute("insert into credit_card values ({}, '{}', '0000 Placeholder Dr', '', 'Placeholder', 'ZZ', '00000', 'USA')".format(card_id_new, card_number_new))
            # then see if the updated customer is in the system, if no then add customer
            cur.execute("select cust_id from customer where cust_name = '{}'".format(cust_name_new))
            try: cust_id_new = cur.fetchone()[0]
            except:
                cur.execute("select max(cust_id) from customer")
                cust_id_new = cur.fetchone()[0] + 1
                cur.execute("insert into customer values ({}, '{}', '')".format(cust_id_new, cust_name_new))
            finally:
                # then add the new cc_belong entry
                cur.execute("select max(cc_belong_id) from cc_belong")
                cc_belong_id_new = cur.fetchone()[0] + 1
                cur.execute("insert into cc_belong values ({}, {}, {})".format(cc_belong_id_new, cust_id_new, card_id_new ))
            update_lst.append("cc_belong_id = {}".format(cc_belong_id_new))
    else:
        update_lst.append("cc_belong_id = {}".format(cc_belong_id_new))

    
    if sa_name_new:
        cur.execute("select sa_id from salesperson where sa_name = '" + sa_name_new + "'")
        try: sa_id_new = cur.fetchone()[0]
        except: return "Error updating order_id {}. New salesperson not in system </br> Return to <a href = \"/edit_order/{}\">View/Edit Page</a>".format(order_id, order_id)
        else: update_lst.append("sa_id = {}".format(sa_id_new))
    

    sql += " and ".join(update_lst)
    sql += ' where order_id = {}'.format(order_id)    
    print(sql)
    cur.execute(sql)
    con.commit()
    return "Order_id {} updated </br> Return to <a href = \"/edit_order/{}\">View/Edit Page</a>".format(order_id, order_id)



@route('/show_ordermerch/<order_id>')
def show_ordermerch(order_id):

    sql = 'select order_date, cust_name, card_number, sa_name, sku, merch_name, msrp_price, order_quantity from orders' 
    sql += ' natural join cc_belong natural join customer natural join credit_card left outer join salesperson using (sa_id) left outer join order_merch using (order_id) left outer join merchandise using (sku) where order_id = {}'.format(order_id)
    sql += ' limit 30'
    print(sql)

    html = "<h2> Order Merchandise Details </h2> <br />"
    html += "<a href = \"/homepage\">Back to Search</a> <br />"
    html += "<a href = \"/edit_order/{}\">View/Edit Order</a> <br />".format(order_id)
    html += "<a href = \"/add_ordermerch/{}\">Add Order Merch</a> <br /><br /><br />".format(order_id)

    html += "<h3> Order Merchandise Details for order_id: {} </h3>".format(order_id)
    html += "<table> <tr> <td> order_date </td> <td> cust_name </td> <td> card_number </td> <td> salesperson </td> <td> sku </td> <td> merch_name </td> <td> msrp_price </td> <td> order_quantity </td> </tr>"
    for row in cur.execute(sql):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"
    return html


@route('/add_ordermerch/<order_id>')
def add_ordermerch(order_id):

    sql = 'select order_date, cust_name, card_number, sa_name, sku, merch_name, msrp_price, order_quantity from orders' 
    sql += ' natural join cc_belong natural join customer natural join credit_card left outer join salesperson using (sa_id) left outer join order_merch using (order_id) left outer join merchandise using (sku) where order_id = {}'.format(order_id)
    sql += ' limit 30'
    print(sql)

    html = "<h2> Add Order Merchandise </h2> <br />"
    html += "<a href = \"/homepage\">Back to Search</a> <br />"
    html += "<a href = \"/edit_order/{}\">View/Edit Order</a> <br />".format(order_id)
    html += "<a href = \"/show_ordermerch/{}\">Show Order Merch</a> <br /><br /><br />".format(order_id)

    html += "<h3> Existing Order Merchandise for order_id {} </h3>".format(order_id)
    html += "<table> <tr> <td> order_date </td> <td> cust_name </td> <td> card_number </td> <td> salesperson </td> <td> sku </td> <td> merch_name </td> <td> msrp_price </td> <td> order_quantity </td> </tr>"
    for row in cur.execute(sql):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
    html += "</table>"

    html += "<br /><br /><br /><br /><br />"
    html += "<h3> Add Order Merchandise for order_id {} </h3>".format(order_id)

    html += '''
        <form action = "/insert_ordermerch/{}" method = "post">
            Merchandise Name: <select id="merch_name" name="merch_name">
        '''.format(order_id)

    sql= "select distinct(merch_name) from merchandise order by merch_name asc"
    for row in cur.execute(sql):
        for cell in row:
            html += "<option value=\"{}\"> {} </option>".format(cell, cell)

    html += '''
            </select>
            Order Quantity: <input name = "order_quantity" type="text" />
            <input value = "Add Merchandise" type = "submit" />
        </form>
    '''
    return html


@post('/insert_ordermerch/<order_id>')
def insert_ordermerch(order_id):
    merch_name = request.forms.get('merch_name').strip()
    order_quantity = request.forms.get('order_quantity').strip()

    # validate order_quantity
    try: order_quantity = int(order_quantity)
    except: return "Error adding merchandise {} to order_id {}. Order Quantity should be positive integer. </br> Return to <a href = \"/add_ordermerch/{}\">Add Order Merch</a>". format(merch_name, order_id, order_id)
    if order_quantity <= 0: return "Error adding merchandise {} to order_id {}. Order Quantity should be positive integer. </br> Return to <a href = \"/add_ordermerch/{}\">Add Order Merch</a>". format(merch_name, order_id, order_id)

    # validate merchandise name
    cur.execute("select sku from merchandise where merch_name = '{}'".format(merch_name))
    try: sku = cur.fetchone()[0]
    except: return "Error adding merchandise {} to order_id {}. Merchandise name not found in system. </br> Return to <a href = \"/add_ordermerch/{}\">Add Order Merch</a>". format(merch_name, order_id, order_id)
    # validate if the added new merchandise is already existing in the order, if so then just update the quantity to old quantity + new quantity
    cur.execute("select order_quantity from order_merch natural join order_merch where order_id = {} and sku = '{}' ".format(order_id, sku))
    try: old_quantity = int(cur.fetchone()[0])
    except: # that means this is a new sku for this order
        sql = "insert into order_merch values ({0}, '{1}', {2})".format(order_id, sku, order_quantity)
    else: # means this is an existing sku for this order, then update quantity
        sql = "update order_merch set order_quantity = {} where order_id = {} and sku = '{}'".format(old_quantity+order_quantity, order_id, sku)
    
    print(sql)
    cur.execute(sql)
    con.commit()

    return "New merchandise {} {} added to order_id {} </br> Return to <a href = \"/add_ordermerch/{}\">Add Order Merch</a>".format(sku, merch_name, order_id, order_id)



run(host='localhost', port=8080, debug = True)