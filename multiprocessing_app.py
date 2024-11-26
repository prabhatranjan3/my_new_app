import multiprocessing 
import time 
import random 
import requests 
import os 
import json 
import csv 


# ======================== 
# Task Functions 
# ======================== 

def download_file(url): 

    """ 
    Downloads a file from the given URL and saves it locally. 
    Args: 
        url (str): The URL of the file to download. 
    Returns: 
        str: A message indicating whether the download was successful or an error occurred. 
    """ 

    print(f"Process {multiprocessing.current_process().name} started downloading from {url}") 
    try: 
        response = requests.get(url, timeout=10) 
        response.raise_for_status()  # Raise exception for HTTP errors 
        file_name = url.split("/")[-1] or f"file_{random.randint(1, 1000)}.txt" 
        with open(file_name, "wb") as file: 
            file.write(response.content) 
        print(f"Process {multiprocessing.current_process().name} finished downloading {file_name}") 
        return f"Downloaded: {file_name}" 
    except Exception as e: 
        return f"Error downloading {url}: {e}" 

 
def process_json_data(file_name): 

    """ 
    Processes a JSON file by filtering and extracting specific data based on conditions. 
    Args: 
        file_name (str): The name of the JSON file to process. 
    Returns: 
        str: A message indicating the status of processing or an error message. 
    """ 

    print(f"Process {multiprocessing.current_process().name} started processing {file_name}") 
    try: 
        with open(file_name, "r") as file: 
            data = json.load(file) 
        filtered_data = [item for item in data if "priority" in item and item["priority"] == "high"] 
        output_file = f"processed_{file_name}" 
        with open(output_file, "w") as file: 
            json.dump(filtered_data, file, indent=4) 
        print(f"Process {multiprocessing.current_process().name} finished processing {file_name}") 
        return f"Processed Data saved to: {output_file}" 
    except Exception as e: 
        return f"Error processing {file_name}: {e}" 


def generate_csv_report(data): 

    """ 
    Generates a CSV report from structured data. 
    Args: 
        data (list): A list of dictionaries containing the data for the report. 
    Returns: 
        str: A message indicating the status of report generation or an error message. 
    """ 

    report_name = f"report_{int(time.time())}.csv" 
    print(f"Process {multiprocessing.current_process().name} started generating report: {report_name}") 
    try: 
        headers = ["ID", "Name", "Status"] 
        with open(report_name, "w", newline="") as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames=headers) 
            writer.writeheader() 
            for row in data: 
                writer.writerow(row) 
        print(f"Process {multiprocessing.current_process().name} finished generating {report_name}") 
        return f"Report Generated: {report_name}" 
    except Exception as e: 
        return f"Error generating report: {e}" 

# ======================== 
# Utility Functions 
# ======================== 

def display_menu(): 

    """
    Displays the user menu for the application. 
    """

    print("\n===== Multiprocessing Application Menu =====") 
    print("1. Download Files from URLs") 
    print("2. Process JSON Data") 
    print("3. Generate CSV Reports") 
    print("4. Exit") 
    print("============================================") 

def create_directory(directory): 
    
    """ 
    Creates a directory if it doesn't exist. 
    Args: 
        directory (str): The name of the directory to create. 
    """ 
    
    if not os.path.exists(directory): 
        os.makedirs(directory) 
        print(f"Created directory: {directory}") 

# ======================== 
# Main Application Logic 
# ========================  

def main(): 

    """ 
    Main function that drives the application. 
    - Displays the menu and takes user input. 
    - Executes tasks based on the user's choice. 
    - Uses multiprocessing for concurrent execution of tasks. 
    """

    # Ensure all output files are stored in a dedicated directory 
    output_dir = "output" 
    create_directory(output_dir) 
    os.chdir(output_dir) 
    while True: 
        display_menu() 
        choice = input("Enter your choice (1-4): ") 
        if choice == "1": 
            # Task: Download files 
            urls = input("Enter URLs to download (comma-separated): ").split(",") 
            urls = [url.strip() for url in urls] 
            with multiprocessing.Pool(processes=4) as pool: 
                results = pool.map(download_file, urls) 
            print("\nDownload Results:") 
            print("\n".join(results)) 
        elif choice == "2": 
            # Task: Process JSON data 
            json_files = input("Enter JSON file names to process (comma-separated): ").split(",") 
            json_files = [file.strip() for file in json_files] 
            with multiprocessing.Pool(processes=4) as pool: 
                results = pool.map(process_json_data, json_files) 
            print("\nData Processing Results:") 
            print("\n".join(results)) 
        elif choice == "3": 
            # Task: Generate CSV reports 
            print("Enter structured data for the report (e.g., [{'ID': 1, 'Name': 'Task1', 'Status': 'Done'}]):") 
            data_input = input() 
            try: 
                data = json.loads(data_input) 
                with multiprocessing.Pool(processes=1) as pool: 
                    results = pool.map(generate_csv_report, [data]) 
                print("\nReport Generation Results:") 
                print("\n".join(results)) 
            except json.JSONDecodeError: 
                print("Invalid input. Please provide valid JSON data.") 
        elif choice == "4": 
            print("Exiting the application. Goodbye!") 
            break 
        else: 
            print("Invalid choice. Please enter a valid option.") 

# ======================== 
# Entry Point 
# ======================== 

if __name__ == "__main__": 
    main() 
