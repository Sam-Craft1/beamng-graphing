import simhub_parser, udp_interface, os, csv_parser, time

socket = udp_interface.init_udp()
areRecording = False
maxSpeed = 0
csv_parser.new_csv()

while True:

    contents = udp_interface.receive_message(socket)
    packet = simhub_parser.parse_telemetry_packet(contents[0])

    if (packet.rpm > packet.idle_rpm + 2000) and not areRecording:
        areRecording = True
        print("Started Recording " + time.strftime("%H:%M:%S"))
        maxSpeed = 0
        startTime = time.time()
    
    if (packet.rpm < packet.idle_rpm + 1000) and areRecording:
        areRecording = False
        if maxSpeed < 30:
            print("Discarded Recording - Max Speed " + str(round(maxSpeed,2)) + " mph")
            csv_parser.new_csv()
        else:
            print("Stopped Recording " + time.strftime("%H:%M:%S"))
            csv_parser.save_csv()
            csv_parser.new_csv()

    if areRecording:
        csv_parser.add_csv_row(packet)
        maxSpeed = max(maxSpeed, packet.wheel_speed_rr) # Assuming rear right wheel speed is representative



#https://plotly.com/python/line-charts/