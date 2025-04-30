from unittest.mock import mock_open, patch
from tasks import load_tasks

def test_load_tasks_with_mock():
    mock_data = '[{"id": 1, "title": "Test Task", "priority": "High"}]'
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_tasks("fake_file.json")
    
    assert isinstance(result, list)
    assert result[0]["id"] == 1
    assert result[0]["title"] == "Test Task"
