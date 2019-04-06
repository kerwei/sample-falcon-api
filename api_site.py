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


# Adds a new item to the catalog
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
@app.route('/customer/edit/<int:item_id>/<string:new_entry>', methods=['GET'])
def editItem(item_id):
    item = session.query(CatalogItem).filter_by(id=item_id).one()

    # Redirects back to the main landing page if the record is not found
    if not item:
        flash("Invalid item. \
            Please check that you have selected a valid item.")
        return redirect(url_for('public_page.itemList'))

    if request.method == 'GET':
        return render_template('edititem.html', item=item)

    if request.method == 'POST':
        user_id = login_session['user_id']

        # Checks that the item belongs to the rightful user
        if user_id == item.user_id:
            item.name = request.form['name']
            item.price = request.form['price']
            item.category = request.form['category']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            flash("Item saved successfully!")
        else:
            flash("You are not authorized to edit this item!")
            return redirect(url_for('public_page.viewCatalogItem',
                category=item.category,
                item_id=item.id))

        return redirect(url_for('public_page.viewCatalogItem',
            category=item.category,
            item_id=item.id))


# Deletes a catalog item
@app.route('/customer/delete/<string:item_id>', methods=['GET'])
def deleteItem(item_id):
    if item_id.isdigit():
        item_id = int(item_id)
    else:
        raise TypeError("Id must be integer")

    item = session.query(Customer).filter_by(id=item_id).one()

    # Redirects back to the main landing page if the record is not found
    if not item:
        flash("Invalid id. \
            Please check that you have entered a valid id.")
        return redirect(url_for('homePage'))

    session.delete(item)
    session.commit()
    flash("Item deleted!")

    return redirect(url_for('homePage'))

# Retrieve a record
@app.route('/', methods=['GET'])
def homePage():
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'my_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
