from db.models.livestream_db import LivestreamDB
from celery import Celery 
from dotenv import load_dotenv
import os 


load_dotenv()

celery = Celery(
    __name__, 
    broker=os.getenv('CELERY_BROKER_URL'),
)

livestream_db = LivestreamDB()

@celery.task
def track_livestream(video_id, channel_id):
    livestream_db.update_livestream_status(video_id, "ongoing")
    livestream_db.process_livechat(video_id, channel_id)
    livestream_db.update_livestream_status(video_id, "ended")