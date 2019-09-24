from flask import Flask , jsonify, request, render_template, redirect,url_for
import pymysql.cursors
from flask_marshmallow import Marshmallow
import os, requests, json
app = Flask(__name__)

# connection to the DB
HOST = "34.66.79.240"
USER = "root"
PASSWORD = "1234"
DATABASE = "guestbook"

connection=None
if(connection == None):
    connection = pymysql.connect(HOST,USER,PASSWORD,DATABASE)




# endpoint to edit the patients 


@app.route("/admin/edit/", methods=['POST'])
def editBook():
    print("Editing")
    id = request.form["BookID"]
    if(request.form["option"] == "title"):
        value = request.form["value"]
        with connection.cursor() as cursor:
            cursor.execute("update patient set fname = %s where id = %s",(value,id))
        connection.commit()
        return redirect(url_for('admin'))
    if(request.form["option"] == "author"):
        value = request.form["value"]
        with connection.cursor() as cursor:
            cursor.execute("update patient set lname = %s where id  = %s",(value,id))
        connection.commit()
        return redirect(url_for('admin'))
    if(request.form["option"] == "pub_date"):
        value = request.form["value"]
        with connection.cursor() as cursor:
            cursor.execute("update patient set price = %s where id  = %s",(value,id))
        connection.commit()
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))
    
# endpoint to get all the patients 
@app.route("/allbooks/", methods=['GET'])
def getBooks():
    print("Getting books")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM patient ")
    connection.commit()
    myresult = cursor.fetchall()
    # return render_template("admin.html")

    results= jsonify(myresult)
    return results


@app.route("/admin/")
def admin():
    return render_template("admin.html")



if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0") 
    
    