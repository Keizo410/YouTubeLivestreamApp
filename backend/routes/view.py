from flask import Blueprint, jsonify, render_template
import os
from utilities.database import Database

views_bp = Blueprint('views', __name__)
db = Database()

@views_bp.route('/drop', methods=['DELETE'])
def drop():
    db.set_sql_file('db/queries/drop.sql')
    success, response = db.drop_table(db.get_sql_file())
    if(response == 200):
        return "Dropped"
    else:
        return "Error!"
    
# @views_bp.route('/view', methods=['GET'])
# def view():
#     db.set_sql_file('db/queries/view.sql')
#     message, response = db.view_table(db.get_sql_file())
#     if(response==200):
#         return render_template('view.html', data=message[0], columns=message[1])
#     else:
#         return message, response
    
@views_bp.route('/')
def welcome():
    db.set_sql_file('db/queries/initialize.sql')
    db.create_tables(db.get_sql_file())
    return jsonify({'message': 'Backend System is Established!'}), 200