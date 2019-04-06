from functools import wraps
from datetime import datetime

from flask import Flask
from flask import request, render_template, redirect, url_for, flash
from flask import abort, jsonify, flash, escape
from flask import session as login_session

import helpers
from database_setup import Base, Customer
from dbfunctions import session


# Starts the application and register the blueprints
app = Flask(__name__)


def parseUrlEntry(entry_string):
    if '|' in entry_string:
        name = entry_string.split('|')[0]
        dob = datetime.strptime(entry_string.split('|')[1], '%d-%m-%Y')
        return [name, dob]
    else:
        return []


# Adds a customer
@app.route('/customer/add/<string:new_entry>', methods=['GET'])
def newItem(new_entry):
    data = parseUrlEntry(new_entry)
    # Creates the record and saves it to the database
    if data:
        new_item = Customer(name=data[0], dob=data[1])
        session.add(new_item)
        session.commit()

    return redirect(url_for('homePage'))


# Edits the catalog item record
@app.route('/customer/edit/<string:item_id>/<string:new_entry>', methods=['GET'])
def editItem(item_id, new_entry):
    if item_id.isdigit():
        item_id = int(item_id)
    else:
        raise TypeError("Id must be integer")
    
    data = parseUrlEntry(new_entry)
    try:
        item = session.query(Customer).filter_by(id=item_id).one()
        item.name = data[0]
        item.dob = data[1]

        session.add(item)
        session.commit()
    except:
        pass

    return redirect(url_for('homePage'))


# Deletes a customer
@app.route('/customer/delete/<string:item_id>', methods=['GET'])
def deleteItem(item_id):
    if item_id.isdigit():
        item_id = int(item_id)
    else:
        raise TypeError("Id must be integer")

    try:
        item = session.query(Customer).filter_by(id=item_id).one()
        session.delete(item)
        session.commit()
    except:
        pass

    return redirect(url_for('homePage'))


# Home
@app.route('/', methods=['GET'])
def homePage():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
