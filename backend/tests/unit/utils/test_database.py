from os import path
import pytest
from utilities.database import Database
from datetime import datetime
from unittest.mock import patch, MagicMock

@pytest.fixture
def database_instance():
    return Database()

def test_youtuber_table_adapter_success(database_instance):
    mockdata = [("1", "youtuber1"), ("2", "youtuber2")]
    expected = [{"id": "1", "name": "youtuber1"}, {"id": "2", "name": "youtuber2"}]
    result = database_instance.youtuberTableAdapter(mockdata)
    assert result == expected

def test_channel_table_adapter_success(database_instance):
    mockdata = [("1", "youtubername1", "youtuber1"), ("2", "youtubername2", "youtuber2")]
    expected = [{"id": "1", "name": "youtubername1", "youtuber": "youtuber1"}, {"id": "2", "name": "youtubername2", "youtuber": "youtuber2"}]
    result = database_instance.channelTableAdapter(mockdata)
    assert result == expected

def test_livestream_table_adapter_success(database_instance):
    queryResult = [
        (1, datetime(2024, 3, 9, 12, 30, 45), datetime(2024, 3, 9), 5, 10, 50.0, "Great stream!")
    ]
    expected = [
        {"id": 1, "currentTime": "12:30:45", "date": "2024-03-09", 
         "channel_id": 5, "listener_id": 10, "donation": 50.0, "comment": "Great stream!"}
    ]
    assert database_instance.livestreamTableAdapter(queryResult) == expected

@patch("utilities.database.Database.get_queries", return_value=["create table test(id int);"])
@patch("utilities.database.Database.execute_multiple_query", return_value=(True, None))
def test_create_tables_success(mock_execute, mock_get_queries, database_instance, capsys):
    """"Test successful table creation."""
    database_instance.create_tables("test.sql")

    captured = capsys.readouterr()
    assert "Database and tables created successfully!" in captured.err

    mock_get_queries.assert_called_once()
    mock_execute.assert_called_once()
    

def test_create_subscription_success():
    """Test successful subscrition."""
    pass

def test_read_data():
    pass

def test_execute_query():
    pass

def test_execute_multiple_queries():
    pass

def test_execute_livestream_queries():
    pass




