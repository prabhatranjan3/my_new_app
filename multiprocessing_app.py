import os
import logging
import requests
from logger import logger

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_file(args):
    """
    Downloads a file from a given URL and saves it locally.

    Args:
        args (tuple): A tuple containing:
            - url (str): The URL to download the file from.
            - save_path (str or os.PathLike): The local path (including file name) to save the downloaded file.

    Returns:
        None: Logs an error or success message.
    """
    if not isinstance(args, tuple) or len(args) != 2:
        logging.error("Invalid arguments. Expected a tuple of (url, save_path).")
        return
    
    url, save_path = args

    # Validate save_path
    if os.path.isdir(save_path) or not isinstance(save_path, (str, os.PathLike)):
        logging.error("Invalid save path. It must be a file path, not a directory.")
        return
    
    try:
        logging.info(f"Downloading from {url} to {save_path}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        logging.info(f"File downloaded successfully and saved at {save_path}")
    except Exception as e:
        logging.error(f"Failed to download the file: {e}")


def process_data(file_path):
    """
    Processes the downloaded file and generates a summary report.

    Args:
        file_path (str or os.PathLike): The path to the file to process.

    Returns:
        dict: A dictionary containing the processed file report:
            - file_name (str): The name of the file.
            - num_rows (int): Number of rows in the file (example value).
            - num_columns (int): Number of columns in the file (example value).
            - columns (list): List of column names (example values).
            - first_5_rows (str): A string representation of the first 5 rows (example values).
            - summary (str): Summary statistics or description of the data.
    """
    if not file_path or not isinstance(file_path, (str, os.PathLike)) or os.path.isdir(file_path):
        logging.error("Invalid file path provided. File path must be a non-empty string or path-like object and must not be a directory.")
        return {"file_name": None, "summary": "Invalid file path"}

    if not os.path.exists(file_path):
        logging.error(f"File {file_path} not found.")
        return {"file_name": file_path, "summary": "File not found"}
    
    try:
        logging.info(f"Processing file: {file_path}")
        # Example: Add some dummy processing logic
        report = {
            "file_name": file_path,
            "num_rows": 100,  # Example
            "num_columns": 5,  # Example
            "columns": ["col1", "col2", "col3", "col4", "col5"],  # Example
            "first_5_rows": "Row1, Row2, Row3, Row4, Row5",  # Example
            "summary": "Summary of the data"  # Example
        }
        return report
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return {"file_name": file_path, "summary": f"Error processing file: {e}"}


def save_report(report, original_file_path):
    """
    Saves the processed data report to a CSV file.

    Args:
        report (dict): The report dictionary generated from the process_data function.
        original_file_path (str or os.PathLike): The original file path of the processed file.

    Returns:
        None: Logs an error or success message.
    """
    if not original_file_path or not isinstance(original_file_path, (str, os.PathLike)) or os.path.isdir(original_file_path):
        logging.error("Invalid original_file_path. It must be a non-empty string or path-like object and must not be a directory.")
        return

    report_file = f"{os.path.splitext(original_file_path)[0]}_report.csv"
    try:
        with open(report_file, 'w') as file:
            file.write(f"Report for {report['file_name']}\n")
            file.write(f"Number of rows: {report.get('num_rows', 'N/A')}\n")
            file.write(f"Number of columns: {report.get('num_columns', 'N/A')}\n")
            file.write(f"Columns: {', '.join(report.get('columns', []))}\n")
            file.write("\nFirst 5 rows of the data:\n")
            file.write(report.get("first_5_rows", "N/A"))
            file.write("\n\nSummary Statistics:\n")
            file.write(report.get("summary", "N/A"))
        
        logging.info(f"Report successfully generated: {report_file}")
    except Exception as e:
        logging.error(f"Error saving report: {e}")


def main():
    """
    Main function to handle user input, download a file, process it, and optionally generate a report.

    Workflow:
    - Accepts a URL and save path from the user.
    - Downloads the file.
    - Optionally processes the downloaded file.
    - Optionally generates and saves a report for the processed data.

    Returns:
        None: Logs messages based on success or failure.
    """
    try:
        # Step 1: Get the URL and save path from the user
        url = input("Enter the URL of the file to download: ").strip()
        save_path = input("Enter the local path to save the downloaded file (include file name and extension): ").strip()
        
        # Validate save_path
        if not url or not save_path or os.path.isdir(save_path):
            logging.error("Invalid save path. Ensure it is not a directory and includes the file name.")
            return
        
        # Step 2: Download the file
        logging.info("Starting file download...")
        download_file((url, save_path))
        
        # Step 3: Ask the user if they want to process the file
        process_choice = input("Do you want to process the downloaded file? (yes/no): ").strip().lower()
        if process_choice not in ['yes', 'y']:
            logging.info("Processing skipped.")
            return

        # Step 4: Process the data
        logging.info("Processing the downloaded file...")
        report = process_data(save_path)

        # Step 5: Ask the user if they want to generate a report
        report_choice = input("Do you want to generate a report for the processed file? (yes/no): ").strip().lower()
        if report_choice in ['yes', 'y']:
            logging.info("Generating report...")
            save_report(report, save_path)
        else:
            logging.info("Report generation skipped.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
