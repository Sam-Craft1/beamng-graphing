import csv, ctypes, matplotlib.pyplot as plt, tkinter as tk, os, main
from tkinter import filedialog
from pathlib import Path

def start_index(data):
    index = 0
    max_wheel_speed = 0.0
    for i in range(len(data)):
        # update max_wheel_speed safely
        if data[i] > max_wheel_speed:
            max_wheel_speed = data[i]
        # detect start index when vehicle begins moving
        if data[i] > 0.8 and index == 0:  # Assuming the car starts moving when rear wheel speed exceeds ~0.8
            index = i
        # reset if wheel speed drops but engine revs high (keep original intent)
        if data[i] < 0.8 and max_wheel_speed < 30 and index != 0:
            index = 0
    return index

def read_csv_data(file_path):
    """Read telemetry data from a CSV file and return it as a list of dictionaries."""
    data = []
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
        
    return data

def graph_telemetry_data(data, selections):

    fig, axs= plt.subplots(nrows=3, ncols=1, figsize=(12, 8), sharex=True)
    
    rpmAxis = axs[0]
    wheelSpeedAxis = axs[1]
    suspensionAxis = axs[2]
    pitchAxis = axs[1].twinx()
    gearAxis = axs[2].twinx()
    gasAxis = axs[0].twinx()
    clutchAxis = axs[0].twinx()
    
    time = [float(row['timeStamp']) for row in data]

    rpm = [float(row['rpm']) for row in data]

    gear = [float(row['gear']) for row in data]

    gasPedal = [float(row['input_throttle']) for row in data]
    clutchPedal = [float(row['input_clutch']) for row in data]

    front_wheel_speed = [float(row['wheel_speed_front']) for row in data]
    rear_wheel_speed = [float(row['wheel_speed_rear']) for row in data]

    front_suspension_position = [float(row['suspension_position_front']) for row in data]
    rear_suspension_position = [float(row['suspension_position_rear']) for row in data] 

    pitch = [float(row['pitchPos']) for row in data]

    index = start_index(rear_wheel_speed)

    zeroTime = time[index]
    time = [t - zeroTime for t in time]

    gearAxis.plot(time, gear, label='Gear', color='magenta')
    gearAxis.tick_params(axis='y', labelcolor='magenta')
    gearAxis.set_facecolor('black')

    gasAxis.plot(time, gasPedal, label='Gas Pedal', color='lime')
    gasAxis.tick_params(axis='y', labelcolor='white')
    gasAxis.set_facecolor('black')

    clutchAxis.plot(time, clutchPedal, label='Clutch Pedal', color='blue')
    clutchAxis.set_facecolor('black')

    pitchAxis.plot(time, pitch, label='Pitch', color='orange')
    pitchAxis.tick_params(axis='y', labelcolor='orange')
    pitchAxis.set_facecolor('black')

    rpmAxis.plot(time, rpm, label='RPM', color='red')
    rpmAxis.tick_params(axis='x', labelcolor='white')
    rpmAxis.tick_params(axis='y', labelcolor='red')
    rpmAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    rpmAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    rpmAxis.set_facecolor('black')

    wheelSpeedAxis.plot(time, front_wheel_speed, label='Front Wheel Speed', color='blue')
    wheelSpeedAxis.plot(time, rear_wheel_speed, label='Rear Wheel Speed', color='cyan')
    wheelSpeedAxis.tick_params(axis='x', labelcolor='white')    
    wheelSpeedAxis.tick_params(axis='y', labelcolor='blue')
    wheelSpeedAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    wheelSpeedAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    wheelSpeedAxis.legend(loc='upper right')
    wheelSpeedAxis.set_facecolor('black')

    suspensionAxis.plot(time, front_suspension_position, label='Front Suspension Position', color='green')
    suspensionAxis.plot(time, rear_suspension_position, label='Rear Suspension Position', color='lime')
    suspensionAxis.tick_params(axis='x', labelcolor='white')
    suspensionAxis.tick_params(axis='y', labelcolor='green')
    suspensionAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    suspensionAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    suspensionAxis.legend(loc='upper right')
    suspensionAxis.set_facecolor('black')


    if not selections['RPM'].get():
        rpmAxis.lines[0].set_visible(False)
        rpmAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Wheel Speed'].get():
        for line in wheelSpeedAxis.lines:
            line.set_visible(False)
        wheelSpeedAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Suspension Position'].get():
        for line in suspensionAxis.lines:
            line.set_visible(False)
        suspensionAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Pitch'].get():
        pitchAxis.lines[0].set_visible(False)
        pitchAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Gear'].get():
        gearAxis.lines[0].set_visible(False)
        gearAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Gas Pedal'].get():
        gasAxis.lines[0].set_visible(False)
        gasAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Clutch Pedal'].get():
        clutchAxis.lines[0].set_visible(False)
        clutchAxis.tick_params(axis='y', labelcolor='black')


    fig.set_facecolor('black')

    fig.tight_layout()
    plt.show()

def graph_comparison_data(data1, data2, selections):
    # Similar implementation as graph_telemetry_data but for two datasets
    # This function will plot data from two different passes for comparison

    #Parsed data order, time, rpm, gear, gasPedal, clutchPedal, front_wheel_speed, rear_wheel_speed, front_suspension_position, rear_suspension_position, pitch

    fig, axs= plt.subplots(nrows=3, ncols=1, figsize=(12, 8), sharex=True) 

    rpmAxis = axs[0]
    wheelSpeedAxis = axs[1]
    suspensionAxis = axs[2]
    gasAxis = axs[0].twinx()
    clutchAxis = axs[0].twinx()
    pitchAxis = axs[1].twinx()
    gearAxis = axs[2].twinx()

    time1 = [float(row['timeStamp']) for row in data1]
    time2 = [float(row['timeStamp']) for row in data2]

    rpm1 = [float(row['rpm']) for row in data1]
    rpm2 = [float(row['rpm']) for row in data2]

    gear1 = [float(row['gear']) for row in data1]
    gear2 = [float(row['gear']) for row in data2]

    gasPedal1 = [float(row['input_throttle']) for row in data1]
    gasPedal2 = [float(row['input_throttle']) for row in data2]
    clutchPedal1 = [float(row['input_clutch']) for row in data1]
    clutchPedal2 = [float(row['input_clutch']) for row in data2]

    front_wheel_speed1 = [float(row['wheel_speed_front']) for row in data1]
    front_wheel_speed2 = [float(row['wheel_speed_front']) for row in data2]
    rear_wheel_speed1 = [float(row['wheel_speed_rear']) for row in data1]
    rear_wheel_speed2 = [float(row['wheel_speed_rear']) for row in data2]

    front_suspension_position1 = [float(row['suspension_position_front']) for row in data1]
    front_suspension_position2 = [float(row['suspension_position_front']) for row in data2]
    rear_suspension_position1 = [float(row['suspension_position_rear']) for row in data1]
    rear_suspension_position2 = [float(row['suspension_position_rear']) for row in data2]

    pitch1 = [float(row['pitchPos']) for row in data1]
    pitch2 = [float(row['pitchPos']) for row in data2]

    parsedData1 = [time1, rpm1, gear1, gasPedal1, clutchPedal1, front_wheel_speed1, rear_wheel_speed1, front_suspension_position1, rear_suspension_position1, pitch1]
    parsedData2 = [time2, rpm2, gear2, gasPedal2, clutchPedal2, front_wheel_speed2, rear_wheel_speed2, front_suspension_position2, rear_suspension_position2, pitch2]

    index1 = start_index(parsedData1[6])  # rear_wheel_speed1
    index2 = start_index(parsedData2[6])  # rear_wheel_speed2


    difference = abs(index1 - index2)

    if index1 < index2:
        for i in range(difference):
            for j in range(len(parsedData1)):
                parsedData1[j].insert(0, parsedData1[j][0] - 0.01)  # Insert a small negative time value to maintain continuity
    elif index2 < index1:
        for i in range(difference):
            for j in range(len(parsedData2)):
                parsedData2[j].insert(0, parsedData2[j][0] - 0.01)  # Insert a small negative time value to maintain continuity   
    else:
        pass

    index1 = start_index(parsedData1[6])  # rear_wheel_speed1
    index2 = start_index(parsedData2[6])  # rear_wheel_speed2

    data1Longer = False

    if len(parsedData1[0]) > len(parsedData2[0]):
        for i in range(len(parsedData1[0]) - len(parsedData2[0])):
            for j in range(len(parsedData2)):
                parsedData2[j].append(0.0)
        data1Longer = True
    elif len(parsedData2[0]) > len(parsedData1[0]):
        for i in range(len(parsedData2[0]) - len(parsedData1[0])):
            for j in range(len(parsedData1)):
                parsedData1[j].append(0.0)
    else:
        pass

    if data1Longer:
        zeroTime = parsedData1[0][index1]
        time = [t - zeroTime for t in parsedData1[0]]
    else:
        zeroTime = parsedData2[0][index2]
        time = [t - zeroTime for t in parsedData2[0]]
 


    for i in range(len(time)):
        if time[i] < -10:
            print(i, time[i])
            

    gasAxis.plot(time, parsedData1[3], label='Gas Pedal Pass 1', color='lime')
    gasAxis.plot(time, parsedData2[3], label='Gas Pedal Pass 2', color='lime', linestyle='dashed')
    gasAxis.tick_params(axis='y', labelcolor='white')
    gasAxis.set_facecolor('black')

    clutchAxis.plot(time, parsedData1[4], label='Clutch Pedal Pass 1', color='blue')
    clutchAxis.plot(time, parsedData2[4], label='Clutch Pedal Pass 2', color='blue', linestyle='dashed')
    clutchAxis.set_facecolor('black')

    gearAxis.plot(time, parsedData1[2], label='Gear Pass 1', color='magenta')
    gearAxis.plot(time, parsedData2[2], label='Gear Pass 2', color='magenta', linestyle='dashed')
    gearAxis.tick_params(axis='y', labelcolor='magenta')
    gearAxis.set_facecolor('black')

    pitchAxis.plot(time, parsedData1[9], label='Pitch Pass 1', color='orange')
    pitchAxis.plot(time, parsedData2[9], label='Pitch Pass 2', color='orange', linestyle='dashed')
    pitchAxis.tick_params(axis='y', labelcolor='orange')
    pitchAxis.set_facecolor('black')

    rpmAxis.plot(time, parsedData1[1], label='RPM Pass 1', color='red')
    rpmAxis.plot(time, parsedData2[1], label='RPM Pass 2', color='red', linestyle='dashed')
    rpmAxis.tick_params(axis='x', labelcolor='white')
    rpmAxis.tick_params(axis='y', labelcolor='red')
    rpmAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    rpmAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    rpmAxis.set_facecolor('black')

    wheelSpeedAxis.plot(time, parsedData1[5], label='Front Wheel Speed Pass 1', color='blue')
    wheelSpeedAxis.plot(time, parsedData2[5], label='Front Wheel Speed Pass 2', color='blue', linestyle='dashed')
    wheelSpeedAxis.plot(time, parsedData1[6], label='Rear Wheel Speed Pass 1', color='cyan')
    wheelSpeedAxis.plot(time, parsedData2[6], label='Rear Wheel Speed Pass 2', color='cyan', linestyle='dashed')
    wheelSpeedAxis.tick_params(axis='x', labelcolor='white')
    wheelSpeedAxis.tick_params(axis='y', labelcolor='cyan')
    wheelSpeedAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    wheelSpeedAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    wheelSpeedAxis.legend(loc='upper right')
    wheelSpeedAxis.set_facecolor('black')

    suspensionAxis.plot(time, parsedData1[7], label='Front Suspension Position Pass 1', color='green')
    suspensionAxis.plot(time, parsedData2[7], label='Front Suspension Position Pass 2', color='green', linestyle='dashed')
    suspensionAxis.plot(time, parsedData1[8], label='Rear Suspension Position Pass 1', color='lime')
    suspensionAxis.plot(time, parsedData2[8], label='Rear Suspension Position Pass 2', color='lime', linestyle='dashed')
    suspensionAxis.tick_params(axis='x', labelcolor='white')
    suspensionAxis.tick_params(axis='y', labelcolor='green')
    suspensionAxis.grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    suspensionAxis.grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    suspensionAxis.legend(loc='upper right')
    suspensionAxis.set_facecolor('black')

    if not selections['RPM'].get():
        for line in rpmAxis.lines:
            line.set_visible(False)
        rpmAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Wheel Speed'].get():
        for line in wheelSpeedAxis.lines:
            line.set_visible(False)
        wheelSpeedAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Suspension Position'].get():
        for line in suspensionAxis.lines:
            line.set_visible(False)
        suspensionAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Pitch'].get():
        for line in pitchAxis.lines:
            line.set_visible(False)
        pitchAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Gear'].get():
        for line in gearAxis.lines:
            line.set_visible(False)
        gearAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Gas Pedal'].get():
        for line in gasAxis.lines:
            line.set_visible(False)
        gasAxis.tick_params(axis='y', labelcolor='black')
    if not selections['Clutch Pedal'].get():
        for line in clutchAxis.lines:
            line.set_visible(False)
        clutchAxis.tick_params(axis='y', labelcolor='black')

    fig.set_facecolor('black')

    fig.tight_layout()
    plt.show()

def graphing_single_gui(recent_pass, prev_pass):

    root = tk.Tk()

    def browse_file():
        file_path = tk.filedialog.askopenfilename(initialdir="./output_logs", filetypes=[("CSV files", "*.csv")]) # type: ignore
        file_label.config(text=file_path)
        return file_path
    
    root.title("Telemetry Comparison")
    root.minsize(400, 300)

    file_label = tk.Label(root, text=(recent_pass if recent_pass else "None"))
    file_label.pack(pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file()).pack(pady=5)
    tk.Label(root, text="Select Data to Graph:").pack(pady=10)
    selections = {
        "RPM": tk.BooleanVar(value=True),
        "Wheel Speed": tk.BooleanVar(value=True),
        "Suspension Position": tk.BooleanVar(value=True),
        "Pitch": tk.BooleanVar(value=True),
        "Gear": tk.BooleanVar(value=True),
        "Gas Pedal": tk.BooleanVar(value=True),
        "Clutch Pedal": tk.BooleanVar(value=False)
    }
    for label, var in selections.items():
        tk.Checkbutton(root, text=label, variable=var).pack(anchor='n')

    tk.Button(root, text="Switch to Compare Graph", command=lambda: single_to_compare(root, file_label.cget("text"), prev_pass)).pack(pady=5)
    tk.Button(root, text="Graph", command=lambda: graph_telemetry_data(read_csv_data(file_label.cget("text")), selections)).pack(pady=20)
    tk.Button(root, text="Exit", command=lambda: return_to_main(root, recent_pass)).pack(pady=5)
    root.mainloop()

def graph_comparison_gui(recent_pass, prev_pass):

    root = tk.Tk()

    root.title("Telemetry Comparison")
    root.minsize(400, 300)

    def browse_file(file_label):
        file_path = tk.filedialog.askopenfilename(initialdir="./output_logs", filetypes=[("CSV files", "*.csv")]) # type: ignore
        file_label.config(text=file_path)
        return file_path

    file_label1 = tk.Label(root, text=recent_pass if recent_pass else "Main Pass: None")
    file_label1.pack(pady=5)
    tk.Button(root, text="Browse Main Pass", command=lambda: browse_file(file_label1)).pack(pady=5)
    file_label2 = tk.Label(root, text=("Comparison Pass: None"))
    file_label2.pack(pady=5)
    tk.Button(root, text="Browse Comparison Pass", command=lambda: browse_file(file_label2)).pack(pady=5)
    tk.Label(root, text="Select Data to Graph:").pack(pady=10)
    selections = {
        "RPM": tk.BooleanVar(value=True),
        "Wheel Speed": tk.BooleanVar(value=True),
        "Suspension Position": tk.BooleanVar(value=True),
        "Pitch": tk.BooleanVar(value=True),
        "Gear": tk.BooleanVar(value=True),
        "Gas Pedal": tk.BooleanVar(value=True),
        "Clutch Pedal": tk.BooleanVar(value=False)
    }
    for label, var in selections.items():
        tk.Checkbutton(root, text=label, variable=var).pack(anchor='n')

    tk.Button(root, text="Switch to Single Graph", command=lambda: compare_to_single(root, file_label1.cget("text"), file_label2.cget("text"))).pack(pady=5)
    tk.Button(root, text="Graph", command=lambda: graph_comparison_data(read_csv_data(file_label1.cget("text")), read_csv_data(file_label2.cget("text")), selections)).pack(pady=20)
    tk.Button(root, text="Exit", command=lambda: return_to_main(root, recent_pass)).pack(pady=5)
    root.mainloop()

def return_to_main(root, recent_pass):
    root.destroy()
    plt.close('all')
    main.main(recent_pass)  # Call main with the recent_pass argument

def single_to_compare(root, recent_pass, prev_pass):
    root.destroy()  # Hide the main window
    graph_comparison_gui(recent_pass, prev_pass)

def compare_to_single(root, recent_pass, prev_pass):
    root.destroy()  # Hide the main window
    graphing_single_gui(recent_pass, prev_pass)







