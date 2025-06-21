from ..base_db import BaseDB

class ListenerDB(BaseDB):
    def __init__(self):
        super().__init__()

    def listenerTableAdapter(self, queryResult):
        return [
            {
                "id": row[0],
                "name": row[1],
                "donation": row[2] if row[2] is not None else 0
            } for row in queryResult
        ]

    def read_listeners(self):
        """
        Retrieves donation contributers 

        Returs:

        """
        query = """
                select 
                    listener.id,
                    listener.name as names, 
                    SUM(livestream.donation) as donations 
                from 
                    listener 
                join livestream on listener.id = livestream.listener_id
                group by listener.id, listener.name
                order by donations desc
                """
        
        return self.read_data(query, self.listenerTableAdapter)