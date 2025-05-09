from flask import Blueprint, jsonify, render_template
import os
from utilities.database import Database

views_bp = Blueprint('views', __name__)
db = Database()

@views_bp.route('/')
def welcome():
    if os.getenv('FLASK_ENV') != 'development':
        return jsonify({'error': 'Forbidden'}), 403
    db.set_sql_file('db/queries/initialize.sql')
    db.create_tables(db.get_sql_file())
    return jsonify({'message': 'Backend System is Established!'}), 200