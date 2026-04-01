import csv, ctypes, matplotlib.pyplot as plt, tkinter as tk, os, main
from tkinter import filedialog

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
    
    ax4 = axs[1].twinx()
    ax5 = axs[2].twinx()
    ax6 = axs[0].twinx()
    ax7 = axs[0].twinx()
    


    time = [float(row['timeStamp']) for row in data]

    rpm = [float(row['rpm']) for row in data]

    gear = [float(row['gear']) for row in data]

    gasPedal = [float(row['input_throttle']) for row in data]
    clutchPedal = [float(row['input_clutch']) for row in data]

    fr_wheel_speed = [float(row['wheel_speed_fr']) for row in data]
    fl_wheel_speed = [float(row['wheel_speed_fl']) for row in data]
    rr_wheel_speed = [float(row['wheel_speed_rr']) for row in data]
    rl_wheel_speed = [float(row['wheel_speed_rl']) for row in data]

    fr_suspension_position = [float(row['suspension_position_fr']) for row in data]
    fl_suspension_position = [float(row['suspension_position_fl']) for row in data]
    rr_suspension_position = [float(row['suspension_position_rr']) for row in data]
    rl_suspension_position = [float(row['suspension_position_rl']) for row in data]

    pitch = [float(row['pitchPos']) for row in data]

    index = 0
    for i in range(len(rr_wheel_speed)):
        if rr_wheel_speed[i] > 0.8 and index == 0:  # Assuming the car starts moving when rear right wheel speed exceeds 1 mph
            index = i
        if rr_wheel_speed[i] < 0.8:
            index = 0
    zeroTime = time[index]
    time = [t - zeroTime for t in time]

    ax5.plot(time, gear, label='Gear', color='magenta')
    ax5.tick_params(axis='y', labelcolor='magenta')
    ax5.set_facecolor('black')

    ax6.plot(time, gasPedal, label='Gas Pedal', color='lime')
    ax6.tick_params(axis='y', labelcolor='white')
    ax6.set_facecolor('black')

    ax7.plot(time, clutchPedal, label='Clutch Pedal', color='blue')
    ax7.set_facecolor('black')

    ax4.plot(time, pitch, label='Pitch', color='orange')
    ax4.tick_params(axis='y', labelcolor='orange')
    ax4.set_facecolor('black')

    axs[0].plot(time, rpm, label='RPM', color='red')
    axs[0].tick_params(axis='x', labelcolor='white')
    axs[0].tick_params(axis='y', labelcolor='red')
    axs[0].grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    axs[0].grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    axs[0].set_facecolor('black')

    axs[1].plot(time, fr_wheel_speed, label='FR Speed', color='blue', linestyle='dashed')
    axs[1].plot(time, fl_wheel_speed, label='FL Speed', color='cyan', linestyle='dashed')
    axs[1].plot(time, rr_wheel_speed, label='RR Speed', color='blue')
    axs[1].plot(time, rl_wheel_speed, label='RL Speed', color='cyan')
    axs[1].tick_params(axis='x', labelcolor='white')    
    axs[1].tick_params(axis='y', labelcolor='blue')
    axs[1].grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    axs[1].grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    axs[1].legend(loc='upper right')
    axs[1].set_facecolor('black')

    axs[2].plot(time, fr_suspension_position, label='FR Sus Pos', color='green', linestyle='dashed')
    axs[2].plot(time, fl_suspension_position, label='FL Sus Pos', color='lime', linestyle='dashed')
    axs[2].plot(time, rr_suspension_position, label='RR Sus Pos', color='green')
    axs[2].plot(time, rl_suspension_position, label='RL Sus Pos', color='lime')
    axs[2].tick_params(axis='x', labelcolor='white')
    axs[2].tick_params(axis='y', labelcolor='green')
    axs[2].grid(axis='y', which='major', color='white', linestyle='--', alpha=0.5)
    axs[2].grid(axis='x', which='both', color='white', linestyle='--', alpha=0.5)
    axs[2].legend(loc='upper right')
    axs[2].set_facecolor('black')


    if not selections['RPM'].get():
        axs[0].lines[0].set_visible(False)
        axs[0].tick_params(axis='y', labelcolor='black')
    if not selections['Wheel Speed'].get():
        for line in axs[1].lines:
            line.set_visible(False)
        axs[1].tick_params(axis='y', labelcolor='black')
    if not selections['Suspension Position'].get():
        for line in axs[2].lines:
            line.set_visible(False)
        axs[2].tick_params(axis='y', labelcolor='black')
    if not selections['Pitch'].get():
        ax4.lines[0].set_visible(False)
        ax4.tick_params(axis='y', labelcolor='black')
    if not selections['Gear'].get():
        ax5.lines[0].set_visible(False)
        ax5.tick_params(axis='y', labelcolor='black')
    if not selections['Gas Pedal'].get():
        ax6.lines[0].set_visible(False)
        ax6.tick_params(axis='y', labelcolor='black')
    if not selections['Clutch Pedal'].get():
        ax7.lines[0].set_visible(False)
        ax7.tick_params(axis='y', labelcolor='black')


    fig.set_facecolor('black')

    fig.tight_layout()
    plt.show()

def graphing_gui(recent_pass):

    root = tk.Tk()

    def browse_file():
        file_path = tk.filedialog.askopenfilename(initialdir="./output_logs", filetypes=[("CSV files", "*.csv")])
        file_label.config(text=file_path)
        return file_path
    
    root.title("Telemetry Graphing")
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
        tk.Checkbutton(root, text=label, variable=var).pack(anchor='w')

    tk.Button(root, text="Graph", command=lambda: graph_telemetry_data(read_csv_data(file_label.cget("text")), selections)).pack(pady=20)
    tk.Button(root, text="Exit", command=lambda: return_to_main(root)).pack(pady=5)
    root.mainloop()

def return_to_main(root):
    root.destroy()
    plt.close('all')
    main.main()








