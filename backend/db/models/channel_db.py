from ..base_db import BaseDB

class ChannelDB(BaseDB):
    def __init__(self):
        super().__init__()
        
    def channelTableAdapter(self, queryResult):
        """
        Converts a list of tuples containing channel relation data into a list of dictionaries.

        This method takes query results in tuple form and transforms them into a structured 
        table-like format using dictionaries.

        Parameters:
        queryResult (list[tuple]): A list of tuples where each tuple represents a channel record.
                                Expected format: (id, name, youtuber).

        Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a channel.
                    Example: [{"id": 1, "name": "TechChannel", "youtuber": "Alice"}]
        """
        return [{"id": row[0], 
                 "name": row[1],
                 "youtuber": row[2],
                 "status": row[3] if row[3] is not None else "offline"
                 } for row in queryResult]

    def read_channel(self):
        """
        Retrieves all channels along with the associated YouTuber's name and livestream status.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of channels) if successful, (False, error message) if an error occurs.
        """
        query = """        
            SELECT
                c.id,
                c.name,
                y.name AS youtuber,
                latest_status.status_name
            FROM
                channel c
            LEFT JOIN youtuber y ON c.youtuber_id = y.id
            LEFT JOIN (
                SELECT
                l.channel_id,
                s.status AS status_name,
                MAX(ls.updated_at) AS latest_update
                FROM
                livestream l
                INNER JOIN livestream_status ls ON l.id = ls.livestream_id
                INNER JOIN status s ON s.id = ls.status_id
                GROUP BY l.channel_id, s.status
            ) latest_status ON latest_status.channel_id = c.id
            ORDER BY c.id"""
        return self.read_data(query, self.channelTableAdapter)
