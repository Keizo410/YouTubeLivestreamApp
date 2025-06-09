from db.models.livestream_db import LivestreamDB
from celery import Celery 

celery = Celery(
    __name__, 
    broker="amqp://guest@rabbitmq//",
)

livestream_db = LivestreamDB()

@celery.task
def track_livestream(video_id, channel_id):
    livestream_db.update_livestream_status(vdId=video_id, status="ongoing")
    livestream_db.process_livechat(video_id, channel_id)
    livestream_db.update_livestream_status(vdId=video_id, status="ended")