import csv, matplotlib.pyplot as plt


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

def graph_single_data(data, selections):

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

    if not selections & (1 << 0):
        rpmAxis.lines[0].set_visible(False)
        rpmAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 1):
        for line in wheelSpeedAxis.lines:
            line.set_visible(False)
        wheelSpeedAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 2):
        for line in suspensionAxis.lines:
            line.set_visible(False)
        suspensionAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 3):
        pitchAxis.lines[0].set_visible(False)
        pitchAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 4):
        gearAxis.lines[0].set_visible(False)
        gearAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 5):
        gasAxis.lines[0].set_visible(False)
        gasAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 6):
        clutchAxis.lines[0].set_visible(False)
        clutchAxis.tick_params(axis='y', labelcolor='black')

    fig.set_facecolor('black')

    fig.tight_layout()

    return fig

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

    if not selections & (1 << 0):
        for line in rpmAxis.lines:
            line.set_visible(False)
        rpmAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 1):
        for line in wheelSpeedAxis.lines:
            line.set_visible(False)
        wheelSpeedAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 2):
        for line in suspensionAxis.lines:
            line.set_visible(False)
        suspensionAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 3):
        for line in pitchAxis.lines:
            line.set_visible(False)
        pitchAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 4):
        for line in gearAxis.lines:
            line.set_visible(False)
        gearAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 5):
        for line in gasAxis.lines:
            line.set_visible(False)
        gasAxis.tick_params(axis='y', labelcolor='black')
    if not selections & (1 << 6):
        for line in clutchAxis.lines:
            line.set_visible(False)
        clutchAxis.tick_params(axis='y', labelcolor='black')

    fig.set_facecolor('black')

    fig.tight_layout()

    return fig








