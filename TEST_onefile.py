import simhub_parser, udp_interface, os, csv_parser

file_path = "./hex_beamng.txt"

with open(file_path, "r") as file:
    contents = file.read()
packet = simhub_parser.parse_telemetry_packet(contents)
csv_parser.add_csv_row(packet)
csv_parser.save_csv()