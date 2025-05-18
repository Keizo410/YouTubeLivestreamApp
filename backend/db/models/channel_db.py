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
                 "youtuber": row[2]} for row in queryResult]

    def read_channel(self):
        """
        Retrieves all channels along with the associated YouTuber's name.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of channels) if successful, (False, error message) if an error occurs.
        """
        query = """SELECT channel.id, channel.name, youtuber.name 
                FROM channel 
                LEFT JOIN youtuber ON channel.youtuber_id = youtuber.id"""
        return self.read_data(query, self.channelTableAdapter)
