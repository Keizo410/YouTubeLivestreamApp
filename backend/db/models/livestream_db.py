from ..base_db import BaseDB
import psycopg2
import pytchat 
import sys

class LivestreamDB(BaseDB):

    def __init__(self):
        super().__init__()
        
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
