import simhub_parser, udp_interface, os, csv_parser, time, graphing_util, tkinter as tk, sys


def graph_helper(sock, root=None, file_path=None, previous_pass=None):
    if root is not None:
        root.destroy()
    udp_interface.close_udp(sock)

    print("Opening Graphing Window...")
    graphing_util.graphing_single_gui(file_path, previous_pass)

def exit_program(sock, root):
    root.destroy()
    udp_interface.close_udp(sock)
    sys.exit()

def main(previous_pass=None):
    socket = udp_interface.init_udp()
    areRecording = False
    maxSpeed = 0
    csv_parser.new_csv()

    root = tk.Tk()

    root.title("SimHub Telemetry Logger")
    tk.Button(root, text="Start Logging", command=lambda: root.destroy()).pack(padx=10, pady=20, side=tk.LEFT)
    tk.Button(root, text="Open Graphs", command=lambda: graph_helper(socket, root, previous_pass)).pack(padx=10, pady=20, side=tk.LEFT)
    tk.Button(root, text="Exit", command=lambda: exit_program(socket, root)).pack(padx=10, pady=20, side=tk.LEFT)
    root.minsize(300, 100)
    root.mainloop()

    print("Starting Telemetry Logging...")

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
            if maxSpeed < 30:
                print("Discarded Recording - Max Speed " + str(round(maxSpeed,2)) + " mph")
                csv_parser.new_csv()
            else:
                print("Stopped Recording " + time.strftime("%H:%M:%S"))
                file_path = csv_parser.save_csv()
                csv_parser.new_csv()
                graph_helper(socket, None, file_path, previous_pass)

        if areRecording:
            csv_parser.add_csv_row(packet)
            maxSpeed = max(maxSpeed, packet.wheel_speed_front) # Assuming front right wheel speed is representative # type: ignore

if __name__ == "__main__":
    main()