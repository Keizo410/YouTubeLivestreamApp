from ..base_db import BaseDB

class YoutuberDB(BaseDB):

    def youtuberTableAdapter(self, queryResult):
        """
        Converts a list of tuples containing YouTuber relation data into a list of dictionaries.

        This method takes query results in tuple form and transforms them into a structured 
        table-like format using dictionaries, making it easier to work with.

        Parameters:
        queryResult (list[tuple]): A list of tuples where each tuple represents a YouTuber record.
                                Expected format: (id, name).

        Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a YouTuber.
                    Example: [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        """
        return [{"id": row[0], 
                 "name": row[1]} for row in queryResult]

    def read_youtuber(self):
        """
        Retrieves all YouTubers and returns them in a structured format.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of youtubers) if successful, (False, error message) if an error occurs.
        """
        query = """SELECT * FROM youtuber"""
        return self.read_data(query, self.youtuberTableAdapter)