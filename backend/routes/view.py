from db.base_db import BaseDB
from flask import Blueprint, jsonify, render_template
import os
from utilities.database import Database

views_bp = Blueprint('views', __name__)
# db = Database()
db = BaseDB()

@views_bp.route('/drop', methods=['DELETE'])
def drop():
    db.set_sql_file('db/queries/drop.sql')
    success, response = db.drop_table(db.get_sql_file())
    if(response == 200):
        return "Dropped"
    else:
        return "Error!"
        
@views_bp.route('/')
def welcome():
    db.set_sql_file('db/queries/initialize.sql')
    db.create_tables(db.get_sql_file())
    return jsonify({'message': 'Backend System is Established!'}), 200