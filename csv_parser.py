import csv, simhub_parser, os, time

csv_rows = []


def add_csv_row(packet):
    row = [round(getattr(packet, field[0]), 2) if isinstance(getattr(packet, field[0]), float) else getattr(packet, field[0]) for field in packet._fields_]
    csv_rows.append(row)

def save_csv():
    if os.path.isdir("./output_logs") == False:
        os.mkdir("./output_logs")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"./output_logs/{timestamp}.csv"
    with open(file_path, "w", newline='') as csvfile:   
        writer = csv.writer(csvfile)
        writer.writerow(simhub_parser.send_headers())
        writer.writerows(csv_rows)
    print(f"CSV saved to {file_path}")

def new_csv():
    global csv_rows
    csv_rows = []