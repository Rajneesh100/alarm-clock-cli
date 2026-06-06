import unittest
from unittest.mock import patch, mock_open

import storage
import manager
import runner

class TestAlarmStorage(unittest.TestCase):
    
    def test_get_next_id_empty(self) -> None:
        self.assertEqual(storage.get_next_id([]), 1)

    def test_get_next_id_existing(self) -> None:
        alarms = [{"id": 1, "time": "12:00"}, {"id": 5, "time": "13:00"}]
        self.assertEqual(storage.get_next_id(alarms), 6)

    @patch("os.path.exists", return_value=False)
    def test_load_alarms_file_not_found(self, mock_exists) -> None:
        self.assertEqual(storage.load_alarms(), [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "time": "12:00", "message": "Test"}]')
    def test_load_alarms_success(self, mock_file, mock_exists) -> None:
        self.assertEqual(storage.load_alarms(), [{"id": 1, "time": "12:00", "message": "Test"}])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_alarms_invalid_json(self, mock_file, mock_exists) -> None:
        self.assertEqual(storage.load_alarms(), [])


class TestAlarmManager(unittest.TestCase):

    def test_validate_time_valid(self) -> None:
        self.assertTrue(manager.validate_time("00:00"))
        self.assertTrue(manager.validate_time("12:34"))
        self.assertTrue(manager.validate_time("23:59"))

    def test_validate_time_invalid(self) -> None:
        self.assertFalse(manager.validate_time("24:00"))
        self.assertFalse(manager.validate_time("12:60"))
        self.assertFalse(manager.validate_time("abc"))
        self.assertFalse(manager.validate_time("12:0"))
        self.assertFalse(manager.validate_time("9:30"))

    @patch("builtins.print")
    @patch("storage.save_alarms")
    @patch("storage.load_alarms", return_value=[])
    def test_add_alarm_success(self, mock_load, mock_save, mock_print) -> None:
        manager.add_alarm("14:30", "Gym time")
        mock_save.assert_called_once_with([{"id": 1, "time": "14:30", "message": "Gym time"}])

    @patch("builtins.print")
    @patch("storage.save_alarms")
    @patch("storage.load_alarms", return_value=[{"id": 1, "time": "12:00", "message": "First"}])
    def test_add_alarm_invalid_time(self, mock_load, mock_save, mock_print) -> None:
        manager.add_alarm("invalid", "Gym time")
        mock_save.assert_not_called()

    @patch("builtins.print")
    @patch("storage.save_alarms")
    @patch("storage.load_alarms", return_value=[{"id": 1, "time": "12:00", "message": "First"}, {"id": 2, "time": "13:00", "message": "Second"}])
    def test_delete_alarm_success(self, mock_load, mock_save, mock_print) -> None:
        manager.delete_alarm("1")
        mock_save.assert_called_once_with([{"id": 2, "time": "13:00", "message": "Second"}])

    @patch("builtins.print")
    @patch("storage.save_alarms")
    @patch("storage.load_alarms", return_value=[{"id": 1, "time": "12:00", "message": "First"}])
    def test_delete_alarm_not_found(self, mock_load, mock_save, mock_print) -> None:
        manager.delete_alarm("99")
        mock_save.assert_not_called()


class TestAlarmRunner(unittest.TestCase):

    def test_check_alarms_matching(self) -> None:
        alarms = [
            {"id": 1, "time": "12:00", "message": "One"},
            {"id": 2, "time": "12:01", "message": "Two"},
            {"id": 3, "time": "12:00", "message": "Three"}
        ]
        triggered = runner.check_alarms("12:00", alarms)
        self.assertEqual(len(triggered), 2)
        self.assertEqual(triggered[0]["id"], 1)
        self.assertEqual(triggered[1]["id"], 3)

    def test_check_alarms_no_match(self) -> None:
        alarms = [
            {"id": 1, "time": "12:00", "message": "One"}
        ]
        triggered = runner.check_alarms("13:00", alarms)
        self.assertEqual(triggered, [])

if __name__ == "__main__":
    unittest.main()
