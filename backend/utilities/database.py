from sqlite3 import paramstyle
import psycopg2
import sys
import csv 
import os
import pytchat 
from dotenv import load_dotenv
import json 


load_dotenv()

class Database:
    def __init__(self):
        self.sql_file = ""
        self.data = ""
        self.query = ""
        self.videoId = ""

    def set_videoId(self, videoId):
        self.videoId = videoId

    def get_videoId(self):
        return self.videoId

    def set_sql_file(self, filepath):
        self.sql_file = filepath

    def get_sql_file(self):
        return self.sql_file
    
    def get_queries(self, filepath):
        return [query.strip() for query in self.load_sql_query(filepath).split(';') if query.strip()]
        
    def load_sql_query(self, sql_file):
        with open(sql_file, 'r') as file:
            return file.read()
        
    def get_db_connection(self):
        return psycopg2.connect(
            database=os.getenv("DATABASE"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT")
        )
    
    def youtuberTableAdapter(self, queryResult):
        return [{"id": row[0], "name": row[1]} for row in queryResult]

    
    def channelTableAdapter(self, queryResult):
        return [{"id": row[0], "name": row[1], "youtuber_id": row[2]} for row in queryResult]
    
    def livestreamTableAdapter(self, queryResult):
        return [{"id": row[0], "current time": row[1], "date": row[2], "channel_id": row[3], "listener_id": row[4], "donation": row[5], "comment": row[6]} for row in queryResult]
    
    def create_tables(self, filepath):
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
        try: 
            if not channelHolderName:
                channelHolderName = ["Unknown Name"]  # Default value if no name is provided
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""INSERT INTO youtuber (name)
                            VALUES (%s) ON CONFLICT (name) DO NOTHING
                            RETURNING id
                        """, (channelHolderName[0],))  
            youtuber_id = cur.fetchone()  # Get the inserted youtuber_id 
            if not youtuber_id:
                cur.execute("SELECT id FROM youtuber WHERE name = %s", (channelHolderName[0],))
                youtuber_id = cur.fetchone()[0]
            cur.execute("""INSERT INTO channel (name, youtuber_id)
                            VALUES (%s, %s) ON CONFLICT (name) DO NOTHING
                        """, (channelName, youtuber_id))  # Use the fetched youtuber_id
            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 

    def update_subscription(self):
        pass

    def delete_subscription(self):
        pass

    #return table of youtubers associated with 0..n channels
    def read_youtuber(self):
        try: 
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""select * from youtuber""")
            table = cur.fetchall()  # Fetch all rows
            result = self.youtuberTableAdapter(table)            
            cur.close()
            conn.close()
            return True, result 
        except (Exception, psycopg2.Error) as error:
            return False, error 

    #return table of channels associated with youtuber name, total earned livestreaming money, total number of livestreaming session, 
    def read_channel(self):
        try: 
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""select * from channel""")
            table = cur.fetchall()  # Fetch all rows
            result = self.channelTableAdapter(table)            
            cur.close()
            conn.close()
            return True, result 
        except (Exception, psycopg2.Error) as error:
            return False, error 

    #return table of livestreams associated with channel names, total earned livestreaming money, number of comments
    def read_livestream(self):
        try: 
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("""select * from livestream""")
            table = cur.fetchall()  # Fetch all rows
            result = self.livestreamTableAdapter(table)            
            cur.close()
            conn.close()
            return True, result 
        except (Exception, psycopg2.Error) as error:
            return False, error 

    #return table of listeners for specific channel
    def read_channelListener(self):
        pass

    #return table of listerners for specific livestreaming
    def read_livestreamListener(self):
        pass

    def view_table(self, filepath):
        try:
            queries = self.get_queries(filepath=filepath)
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute(queries[0])
            results = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            cur.close()
            conn.close()
            data = [dict(zip(columns, row)) for row in results]
            return [data, columns], 200
        except (Exception, psycopg2.Error) as error:
            return f"Error while fetching data: {error}", 500
        
    def execute_single_query(self, query, params=()):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 
        
    def execute_multiple_query(self, query, params=()):
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
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()

            livechat = pytchat.create(video_id=self.get_videoId())
            while livechat.is_alive():
                try:
                    for c in livechat.get().sync_items():
                        if c.amountValue is None:
                            c.amountValue = 0
                        cur.execute("""
                            INSERT INTO livestream (donation, comment)
                            VALUES (%s, %s) 
                        """, (c.message, c.amountValue))
                        cur.execute("""
                            INSERT INTO listener (name)
                            VALUES (%s) ON CONFLICT (name) DO NOTHING
                        """, (c.author.name))
                        conn.commit()
                except KeyboardInterrupt:
                    livechat.terminate()
                    break
                except Exception as e:
                    print(f"Error during live chat processing: {e}", file=sys.stderr)
                    break

            conn.commit()
            cur.close()
            conn.close()
            return True, ""
        except (Exception, psycopg2.Error) as error:
            return False, error 



    
    def execute_query(self, query="", method="", csv_filepath=""):
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

    def summerize_db_data(self, filepath):
        query = self.load_sql_query(filepath).strip()
        queries = [query.strip() for query in query.split(';') if query.strip()]

        if len(queries) < 3:
            print("Insufficient queries found in the file.", file=sys.stderr)
            return

        success, error = self.execute_query(query=queries, method="summary")

        if(success):
            print("Data has been successfully aggregated and inserted into author_totals table", file=sys.stderr)
        else:
            print(f"Error while aggregating data: {error}", file=sys.stderr)
    
    def write_summary_to_csv(self, sql_filepath, csv_filepath):
        queries = self.get_queries(sql_filepath)
        if not queries:
            return None

        success, error = self.execute_query(query=queries, method="csv", csv_filepath=csv_filepath)
        if(success):
            return csv_filepath
        else:
            print(f"Error while writing data to CSV: {error}", file=sys.stderr)
            return None
        
    def process_livechat(self, vd):
        print("Tracking Started...")
        self.set_videoId(str(vd.value))
        success, error = self.exucture_livestream_query()
        if(success):
            print("Tracking Finished...", file=sys.stderr)
        else:
            print("SQL execusion during live streaming was unsuccessfull: ", {error})

    def drop_table(self, filepath):
        queries = self.get_queries(filepath=filepath)
        if queries:
            success, error = self.execute_query(query=queries, method="drop")
            if(success):
                return "Table dropped successfully!", 200
            else:
                return f"Error while dropping table: {error}", 500
        else:   
            return "No queries found in the file.", 400
       
    # def recreate_table(self, filepath):
    #     queries = self.load_sql_query(filepath).split(';')
    #     queries = [query.strip() for query in queries if query.strip()]
    #     if queries:
    #         success, error = self.execute_query(query=queries, method="recreate")
    #         if(success):
    #             return "Tables created successfully!", 200
    #         else:
    #             return f"Error while creating table: {error}", 500
    #     else:
    #         return "No queries found in the file.", 400
        
    # def add_mock_table(self, filepath):
    #     queries = self.load_sql_query(filepath).split(';')
    #     queries = [query.strip() for query in queries if query.strip()]
    #     if len(queries) > 1:
    #        success, error = self.execute_query(query=queries, method="mock")
    #        if(success):
    #             return "Data added successfully!", 200
    #        else:
    #             return f"Error while adding data: {error}", 500
    #     else:
    #         return "No queries found in the file.", 400
    

        # def initialize_db(self, filepath):
    #     queries = self.get_queries(filepath=filepath)
    #     if queries:
    #         success, error = self.execute_multiple_query(query=queries)
    #         if(success):
    #             print("Database and tables created successfully!", file=sys.stderr)
    #         else:
    #             print(f"Error while creating database: {error}", file=sys.stderr)
    #     else:
    #         print("No queries found in the file.", file=sys.stderr)


        
    
               
            

        