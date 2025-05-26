from bottle import route, run, template, post, get, request
import sqlite3
con = sqlite3.connect('webserverdata.db')
cur = con.cursor()

@post('/insert')
def insert():
    sa_name = request.forms.get('salesperson_name')
    salary = request.forms.get('salary')
    dept_id = request.forms.get('dept_id')
    split = request.forms.get('split')
    # print(sa_name, salary, dept_id, split)
    
    # validate the user input 
    try:
        sa_name = sa_name.strip()
        salary = float(salary)
        dept_id = int(dept_id)
        split = float(split)
    except:
        return "Error inserting " + sa_name +  "</br> Return to <a href = \"/listall\">main page</a>"

    # integrity checks
    cur.execute("select distinct(dept_id) from department")
    dept_id_lst = [r[0] for r in cur]
    if not sa_name or salary < 0 or dept_id not in dept_id_lst or split < 0 or split > 1:
        return "Error inserting " + sa_name +  ". Integrity constraint violated. </br> Return to <a href = \"/listall\">main page</a>"

    # if pass integrity checks then add the new salesperson with a new unique sa_id
    cur.execute("select max(sa_id) from salesperson")
    sa_id = cur.fetchone()[0] + 1

    cur.execute("insert into salesperson values ({0}, '{1}', {2}, {3}, {4})".format(sa_id, sa_name, salary, dept_id, split))
    con.commit()
    return sa_name +  " inserted </br> Return to <a href = \"/listall\">main page</a>"

@route('/delete/<sa_id>')
def delete(sa_id):
    cur.execute("delete from salesperson where sa_id = '" + sa_id + "'")
    con.commit()
    return "sa_id " + sa_id + " deleted </br> Return to <a href = \"/listall\">main page</a>"

@route('/listall')
def hello():
    html = "<h2> all salesperson</h2> <br /> <table>"

    html += "<tr> <td> sa_id </td> <td> sa_name </td> <td> salary </td> <td> dept_id </td> <td> split </td>    </tr>"
    for row in cur.execute('select * from salesperson'):
        html += "<tr>"
        for cell in row:
            html += "<td>" + str(cell) + "</td>"
        html += "<td><a href=\"/delete/" + str(row[0]) + "\">delete</a> </td>  </tr>"
    html += "</table>"

    html += "<br /><br /><br /><br /><br />"
    html += '''
        <form action = "/insert" method = "post">
            Salesperson Name: <input name = "salesperson_name" type="text" />
            Salary (greater than 0): <input name = "salary" type="text" />
            Department Id: <input name = "dept_id" type="text" />
            Split (between 0 to 1 exclusive): <input name = "split" type="text" />
            <input value = "Insert" type = "submit" />
        </form>
    '''
    return html

run(host='localhost', port=8080, debug = True)