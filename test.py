import csv
import json
import multiprocessing_app
import os
import unittest
from unittest.mock import patch, mock_open, MagicMock


class TestMultiprocessingApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_output_dir = "test_output"
        if not os.path.exists(self.test_output_dir):
            os.mkdir(self.test_output_dir)
        os.chdir(self.test_output_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir("..")
        for root, dirs, files in os.walk(self.test_output_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_output_dir)

    @patch("requests.get")
    def test_download_file_success(self, mock_get):
        """Test successful file download."""
        mock_get.return_value = MagicMock(status_code=200, content=b"Test content")
        result = multiprocessing_app.download_file("http://example.com/file.txt")
        self.assertIn("Downloaded", result)
        self.assertTrue(os.path.exists("file.txt"))

    @patch("requests.get")
    def test_download_file_failure(self, mock_get):
        """Test failed file download due to HTTP error."""
        mock_get.side_effect = Exception("HTTP error")
        result = multiprocessing_app.download_file("http://example.com/file.txt")
        self.assertIn("Error downloading", result)

    def test_process_json_data_success(self):
        """Test successful JSON file processing."""
        # Create a test JSON file
        input_data = [
            {"priority": "high", "name": "task1"},
            {"priority": "low", "name": "task2"}
        ]
        input_file = "test.json"
        with open(input_file, "w") as file:
            json.dump(input_data, file)

        # Run the function
        result = multiprocessing_app.process_json_data(input_file)

        # Check if the output file exists
        output_file = f"processed_{input_file}"
        self.assertIn("Processed Data saved to", result)
        self.assertTrue(os.path.exists(output_file))

        # Validate the processed data
        with open(output_file, "r") as file:
            processed_data = json.load(file)
        self.assertEqual(len(processed_data), 1)
        self.assertEqual(processed_data[0]["priority"], "high")
        self.assertEqual(processed_data[0]["name"], "task1")

    def test_process_json_data_file_not_found(self):
        """Test JSON processing with a missing file."""
        result = multiprocessing_app.process_json_data("non_existent.json")
        self.assertIn("Error processing", result)

    def test_generate_csv_report_success(self):
        """Test successful CSV report generation."""
        data = [
            {"ID": 1, "Name": "Task1", "Status": "Done"},
            {"ID": 2, "Name": "Task2", "Status": "Pending"}
        ]
        result = multiprocessing_app.generate_csv_report(data)

        # Check if the report file exists
        report_name = result.split(": ")[1]
        self.assertIn("Report Generated", result)
        self.assertTrue(os.path.exists(report_name))

        # Validate the CSV content
        with open(report_name, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Name"], "Task1")

    @patch("os.makedirs")
    def test_create_directory(self, mock_makedirs):
        """Test directory creation."""
        multiprocessing_app.create_directory("new_directory")
        mock_makedirs.assert_called_with("new_directory")

    @patch("builtins.print")
    def test_display_menu(self, mock_print):
        """Test if the display_menu function prints the correct menu."""
        multiprocessing_app.display_menu()
        mock_print.assert_any_call("\n===== Multiprocessing Application Menu =====")
        mock_print.assert_any_call("4. Exit")

# Entry point for tests
if __name__ == "__main__":
    unittest.main()

