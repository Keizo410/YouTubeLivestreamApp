import psycopg2
import sys
import csv 
import os
import pytchat 
from dotenv import load_dotenv

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
    
    def initialize_db(self, filepath):
        queries = self.load_sql_query(filepath).split(';')
        queries = [query.strip() for query in queries if query.strip()]
        if queries:
            success, error = self.execute_query(query=queries, method="init")
            if(success):
                print("Database and tables created successfully!", file=sys.stderr)
            else:
                print(f"Error while creating database: {error}", file=sys.stderr)
        else:
            print("No queries found in the file.", file=sys.stderr)

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
    
    def read_db(self):
        pass

    def execute_query(self, query="", method="", csv_filepath=""):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()

            if(method=="summary"):
                cur.execute(query[0])
                aggregated_data = cur.fetchall()
                cur.execute(query[1])
                cur.executemany(query[2], aggregated_data)
            elif(method=="init"):
                cur.execute(query[0])
            elif(method=="csv"):
                cur.execute(query[1])
                rows = cur.fetchall()
                with open(csv_filepath, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    column_names = [desc[0] for desc in cur.description]
                    csvwriter.writerow(column_names)
                    csvwriter.writerows(rows)
            elif(method=="yt"):
                livechat = pytchat.create(video_id=self.get_videoId())
                while livechat.is_alive():
                    try:
                        for c in livechat.get().sync_items():
                            if c.amountValue is None:
                                c.amountValue = 0
                            cur.execute("""
                                INSERT INTO livechat_data (datetime, author_name, message, amount_value)
                                VALUES (%s, %s, %s, %s)
                            """, (c.datetime, c.author.name, c.message, c.amountValue))
                            conn.commit()
                    except KeyboardInterrupt:
                        livechat.terminate()
                        break
                    except Exception as e:
                        print(f"Error during live chat processing: {e}", file=sys.stderr)
                        break
            elif(method=="recreate"):
                cur.execute(query[0])
            elif(method=="drop"):
                cur.execute(query[0])
            elif(method=="mock"):
                cur.execute(query[1])
           
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

        query = self.load_sql_query(sql_filepath).split(';')
        queries = [query.strip() for query in query if query.strip()]

        if not query:
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
        success, error = self.execute_query(method="yt")
        if(success):
            print("Tracking Finished...", file=sys.stderr)
        else:
            print("SQL execusion during live streaming was unsuccessfull: ", {error})

    def drop_table(self, filepath):
        queries = self.load_sql_query(filepath).split(';')
        queries = [query.strip() for query in queries if query.strip()]
        if queries:
            success, error = self.execute_query(query=queries, method="drop")
            if(success):
                return "Table dropped successfully!", 200
            else:
                return f"Error while dropping table: {error}", 500
        else:   
            return "No queries found in the file.", 400
       
    def recreate_table(self, filepath):
        queries = self.load_sql_query(filepath).split(';')
        queries = [query.strip() for query in queries if query.strip()]
        if queries:
            success, error = self.execute_query(query=queries, method="recreate")
            if(success):
                return "Tables created successfully!", 200
            else:
                return f"Error while creating table: {error}", 500
        else:
            return "No queries found in the file.", 400
        
    def add_mock_table(self, filepath):
        queries = self.load_sql_query(filepath).split(';')
        queries = [query.strip() for query in queries if query.strip()]
        if len(queries) > 1:
           success, error = self.execute_query(query=queries, method="mock")
           if(success):
                return "Data added successfully!", 200
           else:
                return f"Error while adding data: {error}", 500
        else:
            return "No queries found in the file.", 400
    
    def view_table(self, filepath):
        try:
            query = self.load_sql_query(filepath).split(';')
            queries = [query.strip() for query in query if query.strip()]
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

        
    
               
            

        