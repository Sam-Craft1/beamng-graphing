import csv, ctypes, matplotlib.pyplot as plt

def read_csv_data(file_path):
    """Read telemetry data from a CSV file and return it as a list of dictionaries."""
    data = []
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

