import os
import pandas as pd
import unittest
from downloader import download_file
from logger import logger
from processor import process_data
from report_generator import save_report
from unittest.mock import patch, mock_open



class TestProject(unittest.TestCase):
    """
    Unit test class for testing the functions in downloader, processor, 
    and report_generator modules, as well as the main workflow.

    Tests include:
    - File download functionality.
    - Data processing functionality.
    - Report generation and saving functionality.
    - Integration of the main workflow.
    """

    @patch("requests.get")
    def test_download_valid_file(self, mock_get):
        """
        Test downloading a valid file from a URL and saving it locally.

        Mock:
            - Simulates a successful HTTP response with mock data.

        Asserts:
            - File is saved at the specified path.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.iter_content = lambda chunk_size: [b"data"]
        with patch("builtins.open", mock_open()) as mock_file:
            download_file(("http://example.com/file.csv", "file.csv"))
            mock_file.assert_called_with("file.csv", "wb")

    def test_download_invalid_save_path(self):
        """
        Test downloading a file with an invalid save path.

        Asserts:
            - Logs an error message for invalid save path.
        """
        with self.assertLogs(level="ERROR") as log:
            download_file(("http://example.com/file.csv", "/invalid/directory/"))
        self.assertIn("Invalid save path. It must be a file path, not a directory.", log.output[0])

    def test_download_invalid_arguments(self):
        """
        Test downloading with invalid arguments.

        Asserts:
            - Logs an error message for invalid argument types or structure.
        """
        with self.assertLogs(level="ERROR") as log:
            download_file("http://example.com/file.csv")  # Invalid: not a tuple
        self.assertIn("Invalid arguments. Expected a tuple of (url, save_path).", log.output[0])

    @patch("pandas.read_csv")
    def test_process_valid_csv(self, mock_read_csv):
        """
        Test processing a valid CSV file.

        Mock:
            - Simulates a DataFrame with predefined structure.

        Asserts:
            - Report contains correct row and column counts, column names, and summary.
        """
        mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        report = process_data("valid.csv")
        self.assertEqual(report["num_rows"], 2)
        self.assertEqual(report["num_columns"], 2)
        self.assertEqual(report["columns"], ["col1", "col2"])

    def test_process_non_existent_file(self):
        """
        Test processing a file that does not exist.

        Asserts:
            - Logs an error and returns a "File not found" summary.
        """
        with self.assertLogs(level="ERROR") as log:
            report = process_data("missing.csv")
        self.assertIn("File missing.csv not found.", log.output[0])

    def test_process_invalid_file_type(self):
        """
        Test processing an invalid file path (e.g., directory instead of a file).

        Asserts:
            - Logs an error for invalid file path.
        """
        with self.assertLogs(level="ERROR") as log:
            report = process_data("/invalid/file/path/")
        self.assertIn("Invalid file path provided. File path must be a non-empty string or path-like object", log.output[0])

    def test_save_valid_report(self):
        """
        Test saving a valid report to a file.

        Mock:
            - Simulates opening and writing to a file.

        Asserts:
            - File is saved with the expected name and content.
        """
        report = {
            "file_name": "data.csv",
            "num_rows": 10,
            "num_columns": 2,
            "columns": ["col1", "col2"],
            "first_5_rows": "row1\nrow2",
            "summary": "Summary..."
        }
        with patch("builtins.open", mock_open()) as mock_file:
            save_report(report, "data.csv")
            mock_file.assert_called_with("data_report.csv", "w")

    def test_save_invalid_path(self):
        """
        Test saving a report to an invalid path.

        Asserts:
            - Logs an error message for invalid file path.
        """
        with self.assertLogs(level="ERROR") as log:
            save_report({}, "/invalid/path/")
        self.assertIn("Invalid original_file_path. It must be a non-empty string or path-like object", log.output[0])

    def test_save_report_write_error(self):
        """
        Test handling errors while saving a report.

        Mock:
            - Simulates a PermissionError during file writing.

        Asserts:
            - Logs an error message indicating the write failure.
        """
        report = {
            "file_name": "data.csv",
            "num_rows": 10,
            "num_columns": 2,
            "columns": ["col1", "col2"],
            "first_5_rows": "row1\nrow2",
            "summary": "Summary..."
        }
        with patch("builtins.open", side_effect=PermissionError("Permission denied")):
            with self.assertLogs(level="ERROR") as log:
                save_report(report, "data.csv")
            self.assertIn("Error saving report", log.output[0])

    @patch("builtins.input", side_effect=["http://example.com/file.csv", "file.csv", "yes", "yes"])
    @patch("downloader.download_file")
    @patch("processor.process_data", return_value={
        "file_name": "file.csv",
        "num_rows": 10,
        "num_columns": 2,
        "columns": ["col1", "col2"],
        "first_5_rows": "row1\nrow2",
        "summary": "Summary..."
    })
    @patch("report_generator.save_report")
    def test_main_workflow_success(self, mock_save_report, mock_process_data, mock_download_file, mock_input):
        """
        Test successful execution of the main workflow.

        Mock:
            - Simulates user input for URL, save path, processing, and report generation.
            - Mocks all major functions.

        Asserts:
            - Functions are called with the expected arguments.
        """
        from main import main  # Import main only when testing it
        main()
        mock_download_file.assert_called_once_with(("http://example.com/file.csv", "file.csv"))
        mock_process_data.assert_called_once_with("file.csv")
        mock_save_report.assert_called_once()

    @patch("builtins.input", side_effect=["http://example.com/file.csv", "invalid/path/", "no"])
    def test_main_invalid_save_path(self, mock_input):
        """
        Test main workflow with an invalid save path.

        Asserts:
            - Logs an error for invalid save path.
        """
        from main import main
        with self.assertLogs(level="ERROR") as log:
            main()
        self.assertIn("Invalid save path. Ensure it is not a directory", log.output[0])

    @patch("builtins.input", side_effect=["http://example.com/file.csv", "file.csv", "no"])
    @patch("downloader.download_file")
    def test_main_skip_processing(self, mock_download_file, mock_input):
        """
        Test main workflow where processing and report generation are skipped.

        Asserts:
            - Only the download function is called.
        """
        from main import main
        main()
        mock_download_file.assert_called_once_with(("http://example.com/file.csv", "file.csv"))


if __name__ == "__main__":
    unittest.main()