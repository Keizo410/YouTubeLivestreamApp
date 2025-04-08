from collections import defaultdict
from sqlite3 import paramstyle
import psycopg2
import sys
import csv 
import os
import pytchat 
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

load_dotenv()

class Database:
    """Creates Database instance"""
    def __init__(self):
        """
        Initialize the Database object.

        """
        self.sql_file = ""
        self.data = ""
        self.query = ""
        self.videoId = ""
        self.channelId = ""

    def set_videoId(self, videoId):
        """
        Set YouTube video ID to object.

        Parameters: 
        videoId - a string for YouTube video ID
        """
        self.videoId = videoId

    def get_videoId(self):
        """
        Get method to retrieve YouTube video ID.
        """
        return self.videoId
    
    def set_channelId(self, channelId):
        """
        Set YouTube channel ID to object.

        Parameters: 
        channelId - a string for YouTube channel ID
        """
        self.channelId = channelId

    def get_channelId(self):
        """
        Get method to retrieve YouTube channel ID.
        """
        return self.channelId

    def set_sql_file(self, filepath):
        """
        Set sql file path to object.

        Parameters: 
        filepath - a string for sql script path
        """
        self.sql_file = filepath

    def get_sql_file(self):
        """
        Get method to retrieve sql script path.
        """
        return self.sql_file
    
    def get_queries(self, filepath):
        """
        Get method to retrieve sql queries from a file.

        Parameters:
        filepath - a string for sql script path.
        """
        return [query.strip() for query in self.load_sql_query(filepath).split(';') if query.strip()]
        
    def load_sql_query(self, sql_file):
        """
        Helper method for get_queries to load sql queries from a file.

        Parameters:
        sql_file - a string for sql script path.
        """
        with open(sql_file, 'r') as file:
            return file.read()
        
    def get_db_connection(self):
        """
        Getter method for database connection.
        """
        return psycopg2.connect(
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
    
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
    
    def livestreamTableAdapter(self, queryResult):
        """
        Converts retrieved livestream relation data into a structured table format.

        Parameters:
        queryResult (list[tuple]): A list of tuples where each tuple represents a livestream record.
                                Expected format: (id, currentTime, date, channel_id, listener_id, donation, comment).

        Returns:
        list[dict]: A list of dictionaries representing livestreams.
                    Example: [{"id": 1, "currentTime": "12:30:45", "date": "2024-03-09", 
                            "channel_id": 5, "listener_id": 10, "donation": 50.0, "comment": "Great stream!"}]
        """
        return [{"id": row[0], 
                 "currentTime": row[1].strftime("%H:%M:%S") if row[1] else None,
                 "date": row[2].strftime("%Y-%m-%d"), 
                 "channel_id": row[3], 
                 "listener_id": row[4], 
                 "donation": row[5], 
                 "comment": row[6]} for row in queryResult]
    
    def livestreamChartSummaryAdapter(self, queryResult):
        """
        Converts retrieved livestream relation data into a structured table format.

        Parameters:
        queryResult (list[tuple]): A list of tuples where each tuple represents a livestream record.
                                Expected format: (date, name, sales).

        Returns:
        list[dict]: A list of dictionaries representing livestreams.
                    Example: [{"date": 11/02/11, "YoutuberA": 1000, "YoutuberB": 2000}]
        """
        df = pd.DataFrame(queryResult, columns=['date', 'channel_name', 'sales'])
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        pivot_df = df.pivot(index='date', columns='channel_name', values='sales').fillna(0)
        chart_data = pivot_df.reset_index().to_dict(orient='records')
        return chart_data
    
    def livestreamBarSummaryAdapter(self, queryResult):
        """
        Converts retrieved livestream relation data into a structured table format.

        Parameters:
        queryResult (list[tuple]): A list of tuples where each tuple represents a livestream record.
                                Expected format: (date, name, sales).

        Returns:
        list[dict]: A list of dictionaries representing livestreams.
                    Example: [{"name": "YoutuberA", "sales": 2000}]
        """
        return [{
            "name": row[0],
            "sales": row[1]
        } for row in queryResult]

    def create_tables(self, filepath):
        """
        Reads SQL queries from a file and executes them to create database tables.

        Parameters:
        filepath (str): The path to the file containing SQL queries.

        Returns:
        None: Prints success or error messages to stderr.
        """
        queries = self.get_queries(filepath=filepath)
        if queries:
            success, error = self.execute_multiple_query(query=queries)
            if(success):
                print("Database and tables created successfully!", file=sys.stderr)
            else:
                print(f"Error while creating database: {error}", file=sys.stderr)
        else:
            print("No queries found in the file.", file=sys.stderr)
    

    def create_subscription(self, channelID, channelName, channelHolderName):
        """
        Inserts a new subscription into the database.

        Parameters:
        channelID (str): The unique ID of the YouTube channel.
        channelName (str): The name of the YouTube channel.
        channelHolderName (list[str] | None): The name of the YouTuber (list with one string element).

        Returns:
        tuple[bool, str]: (True, "") if successful, (False, error message) if an error occurs.
        """
        try: 
            conn = self.get_db_connection()
            cur = conn.cursor()
            youtuber_id=None

            if not channelHolderName:
                channelHolderName = ["Unknown"]  
            else:
                cur.execute("""INSERT INTO youtuber (name)
                                VALUES (%s) ON CONFLICT (name) DO NOTHING
                                RETURNING id
                            """, (channelHolderName[0],))  
                youtuber_id = cur.fetchone()  

            if not youtuber_id:
                cur.execute("SELECT id FROM youtuber WHERE name = %s", (channelHolderName[0],))
                youtuber_id = cur.fetchone()[0]

            cur.execute("""INSERT INTO channel (name, channelId, youtuber_id)
                            VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING
                        """, (channelName, channelID, youtuber_id))  
            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 

    def read_data(self, query, adapter_method):
        """
        Generic method to execute a SELECT query and adapt the results using the provided adapter method.

        Parameters:
        query (str): The SQL query to execute.
        adapter_method (function): The method to adapt the fetched data into a structured format.

        Returns:
        tuple[bool, list[dict] | str]: (True, adapted result) if successful, (False, error message) if an error occurs.
        """
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute(query)  
            table = cur.fetchall() 
            result = adapter_method(table)  
            cur.close()
            conn.close()
            return True, result
        except (Exception, psycopg2.Error) as error:
            return False, str(error)
    
    def read_youtuber(self):
        """
        Retrieves all YouTubers and returns them in a structured format.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of youtubers) if successful, (False, error message) if an error occurs.
        """
        query = """SELECT * FROM youtuber"""
        return self.read_data(query, self.youtuberTableAdapter)

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

    def read_livestream(self):
        """
        Retrieves all livestream records.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of livestreams) if successful, (False, error message) if an error occurs.
        """
        query = """SELECT * FROM livestream"""
        return self.read_data(query, self.livestreamTableAdapter)
    
    def read_livestream_chart_summary(self):
        """
        Retrieves livestream records and convert into chart summary data format.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of livestreams) if successful, (False, error message) if an error occurs.
        """
        query = """
                SELECT
                livestream.date AS date,
                channel.name AS channel_name,
                SUM(livestream.donation) AS sales
                FROM livestream 
                JOIN channel  ON livestream.channel_id = channel.id
                GROUP BY livestream.date, channel.name
                ORDER BY livestream.date; 
                """
        return self.read_data(query, self.livestreamChartSummaryAdapter)

    def read_livestream_bar_summary(self):
        """
        Retrieves livestream records and convert into bar summary data format.

        Returns:
        tuple[bool, list[dict] | str]: (True, list of livestreams) if successful, (False, error message) if an error occurs.
        """
        query = """
                SELECT
                channel.name AS channel_name,
                SUM(livestream.donation) AS sales
                FROM livestream 
                JOIN channel  ON livestream.channel_id = channel.id
                GROUP BY channel.name
                ORDER BY sales desc; 
                """
        return self.read_data(query, self.livestreamBarSummaryAdapter)
    
    # def view_table(self, filepath):
    #     """
    #     Reads and executes a query from the given file to retrieve data from the database.
        
    #     Args:
    #         filepath (str): Path to the file containing the SQL query.

    #     Returns:
    #         tuple: A list containing the retrieved data as dictionaries and column names, along with a status code.
    #             If an error occurs, returns an error message and a 500 status code.
    #     """
    #     try:
    #         queries = self.get_queries(filepath=filepath)
    #         conn = self.get_db_connection()
    #         cur = conn.cursor()
    #         cur.execute(queries[0])
    #         results = cur.fetchall()
    #         columns = [desc[0] for desc in cur.description]
    #         cur.close()
    #         conn.close()
    #         data = [dict(zip(columns, row)) for row in results]
    #         return [data, columns], 200
    #     except (Exception, psycopg2.Error) as error:
    #         return f"Error while fetching data: {error}", 500
        
    def execute_multiple_query(self, query, params=()):
        """
        Executes multiple SQL queries in a single transaction.

        Args:
            query (list): A list of SQL queries to execute.
            params (tuple, optional): Parameters for parameterized queries. Defaults to an empty tuple.

        Returns:
            tuple: A boolean indicating success or failure, and an error message if applicable.
        """
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()

            for q in query:
                cur.execute(q, params)

            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 
        
    def exucture_livestream_query(self):
        """
        Fetches live chat messages from a YouTube livestream and stores them in the database.

        Retrieves the video ID and channel name, fetches messages from the live chat, and inserts
        data into the 'listener' and 'livestream' tables.

        Returns:
            tuple: A boolean indicating success or failure, and an error message if applicable.
        """
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            video_id=self.get_videoId()
            livechat = pytchat.create(video_id)
            channelName = self.get_channelId()
            while livechat.is_alive():
                try:
                    cur.execute("""select id from channel where name = %s""",(channelName,))
                    result = cur.fetchone()
        
                    if result is None:
                        print(f"Error: No channel found for channelId {channelName}")
                        break 

                    channel_id = result[0]

                    for c in livechat.get().sync_items():
                        c.amountValue = getattr(c, "amountValue", 0) or 0
                        c.message = c.message or ""
                        author_name = c.author.name if c.author else "Unknown"

                        cur.execute("""INSERT INTO listener (name) VALUES (%s) ON CONFLICT (name) DO NOTHING""", (author_name,))
                        cur.execute("""SELECT id FROM listener WHERE name = %s""", (author_name,))
                        listener_data = cur.fetchone()
                        
                        listener_id = listener_data[0] if listener_data else 1  

                        cur.execute("""
                            INSERT INTO livestream (channel_id, listener_id, donation, comment)
                            VALUES (%s, %s, %s, %s) 
                        """, (channel_id, listener_id, c.amountValue, c.message))

                    conn.commit()
                except KeyboardInterrupt:
                    livechat.terminate()
                    break
                except Exception as e:
                    print(f"Error during live chat processing: {e}", file=sys.stderr)
                    break

            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 
    
    def execute_query(self, query="", method="", csv_filepath=""):
        """
        Executes a database query based on the specified method.
        
        Supported methods:
        - "summary": Executes a summary aggregation query.
        - "csv": Exports query results to a CSV file.
        - "drop": Executes a drop table or deletion query.

        Args:
            query (list or str): A list of queries or a single query string.
            method (str): The execution mode ("summary", "csv", or "drop").
            csv_filepath (str, optional): File path for CSV export if method is "csv".

        Returns:
            tuple: A boolean indicating success or failure, and an error message if applicable.
        """
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            if(method=="summary"):
                cur.execute(query[0])
                aggregated_data = cur.fetchall()
                cur.execute(query[1])
                cur.executemany(query[2], aggregated_data)
            elif(method=="csv"):
                cur.execute(query[1])
                rows = cur.fetchall()
                with open(csv_filepath, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    column_names = [desc[0] for desc in cur.description]
                    csvwriter.writerow(column_names)
                    csvwriter.writerows(rows)
            elif(method=="drop"):
                cur.execute(query[0])
            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
                return False, error 
    
    def write_summary_to_csv(self, sql_filepath, csv_filepath):
        """
        Extracts SQL queries from the provided file, executes them, and writes the results to a CSV file.

        Args:
            sql_filepath (str): The file path of the SQL file containing the queries.
            csv_filepath (str): The file path where the CSV output should be saved.

        Returns:
            str or None: Returns the CSV file path if the operation was successful, otherwise None.
            
        Raises:
            None
        """
        queries = self.get_queries(sql_filepath)
        if not queries:
            return None

        success, error = self.execute_query(query=queries, method="csv", csv_filepath=csv_filepath)
        if(success):
            return csv_filepath
        else:
            print(f"Error while writing data to CSV: {error}", file=sys.stderr)
            return None
        
    def process_livechat(self, vd, ch):
        """
        Tracks live chat data for a given video and channel by setting video and channel IDs
        and executing the livestream query.

        Args:
            vd (object): An object containing the video ID.
            ch (object): An object containing the channel ID.

        Returns:
            None
            
        Raises:
            None
        """
        print("Tracking Started...")
        self.set_videoId(str(vd.value))
        self.set_channelId(str(ch.value))
        success, error = self.exucture_livestream_query()
        if(success):
            print("Tracking Finished...", file=sys.stderr)
        else:
            print("SQL execusion during live streaming was unsuccessfull: ", {error})

    def drop_table(self, filepath):
        """
        Drops the 'livestream', 'channel', 'listener', and 'youtuber' tables from the database if they exist.

        This method ensures the specified tables are removed from the database, handling potential exceptions
        during the execution of the SQL query.

        Args:
            filepath (str): The file path related to this operation (not used in this function but could be used for logging).

        Returns:
            tuple: A tuple containing a boolean indicating success (True/False) and an HTTP status code (200/400).
            
        Raises:
            Exception: If an error occurs during the database operation, it is caught and printed.
        """
        queries = self.get_queries(filepath)
        if not queries:
            return None
        
        success, error = self.execute_query(query=queries, method="drop")
        if(success):
            return True, 200
        else:
            print(f"Error while dropping tables: {error}", file=sys.stderr)
            return False, 400