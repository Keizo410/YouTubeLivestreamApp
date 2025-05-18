import psycopg2
import os
import csv 

class BaseDB():
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