import simhub_parser, udp_interface, csv_parser, time

def log_pass():

    socket = udp_interface.init_udp()
    areRecording = False
    maxSpeed = 0
    csv_parser.new_csv()

    while True:
    
            contents = udp_interface.receive_message(socket)
            packet = simhub_parser.parse_telemetry_packet(contents[0])
    
            if (packet.rpm > packet.idle_rpm + 2000) and not areRecording: # type: ignore
                areRecording = True
                print("Started Recording " + time.strftime("%H:%M:%S"))
                maxSpeed = 0
                startTime = time.time()
            
            if (packet.rpm < packet.idle_rpm + 1000) and areRecording: # type: ignore
                areRecording = False
                if maxSpeed < 80:
                    print("Discarded Recording - Max Speed " + str(round(maxSpeed,2)) + " mph")
                    csv_parser.new_csv()
                else:
                    print("Stopped Recording " + time.strftime("%H:%M:%S"))
                    file_path = csv_parser.save_csv()
                    udp_interface.close_udp(socket)
                    return file_path
    
            if areRecording:
                csv_parser.add_csv_row(packet)
                maxSpeed = max(maxSpeed, packet.wheel_speed_front) # Assuming front right wheel speed is representative # type: ignore

