from db.base_db import BaseDB
from flask import Blueprint
import os
from utilities.emailHandler import Email
from utilities.database import Database

emails_bp = Blueprint('emails', __name__)
# db = Database()
db = BaseDB()

@emails_bp.route('/send_email', methods=['GET'])
def send_email():
    csv_file_path = 'livechat_data.csv'
    email = Email()
    email.set_credentials(os.getenv("SENDER_EMAIL"), os.getenv('APP_PASSWORD'),os.getenv("RECEIVER_EMAIL"))
    email.set_draft("Test Subject", "New summary is generated.")

    db.set_sql_file('db/queries/view.sql')
    csv_file_path = db.write_summary_to_csv(db.get_sql_file(), csv_filepath=csv_file_path)
    
    message, response = email.write_email(csv_file_path=csv_file_path)
    if(response == 200):
        return email.send_email()
    else:
        return message, 500