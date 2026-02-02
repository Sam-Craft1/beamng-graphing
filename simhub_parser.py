import ctypes

content_byte = b''

class TelemetryPacket(ctypes.LittleEndianStructure):
    _pack_ = 1  # remove padding — remove this if the C side is naturally aligned
    _fields_ = [
        ("magic", ctypes.c_char * 8),
        ("timeStamp", ctypes.c_float),

        ("vehicleName", ctypes.c_char * 256),
        ("vehicleModel", ctypes.c_char * 256),
        ("vehicleConfig", ctypes.c_char * 256),

        ("idle_rpm", ctypes.c_float),
        ("max_rpm", ctypes.c_float),
        ("gear", ctypes.c_int32),
        ("max_gears", ctypes.c_int32),
        ("gearboxGrinding", ctypes.c_int32),

        ("speed", ctypes.c_float),
        ("rpm", ctypes.c_float),
        ("turbo", ctypes.c_float),
        ("turboMax", ctypes.c_float),
        ("engTemp", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("oilTemp", ctypes.c_float),
        ("waterTemp", ctypes.c_float),
        ("fuelCapacity", ctypes.c_float),
        ("fuelVolume", ctypes.c_float),
        ("engineLoad", ctypes.c_float),
        ("ignitionOn", ctypes.c_int32),

        # Lights
        ("light_HighBeam", ctypes.c_int32),
        ("light_Parkingbrake", ctypes.c_int32),
        ("light_Signal_L", ctypes.c_int32),
        ("light_Signal_R", ctypes.c_int32),
        ("light_Abs", ctypes.c_int32),
        ("light_Oil", ctypes.c_int32),
        ("light_EngineRunning", ctypes.c_int32),
        ("light_TC", ctypes.c_int32),
        ("light_Shift", ctypes.c_int32),
        ("light_HazardEnabled", ctypes.c_int32),

        ("light_LowHighBeam", ctypes.c_int32),
        ("light_LowBeam", ctypes.c_int32),
        ("light_Fog", ctypes.c_int32),

        # Inputs
        ("input_throttle", ctypes.c_float),
        ("input_brake", ctypes.c_float),
        ("input_clutch", ctypes.c_float),
        ("input_parkingBrake", ctypes.c_float),
        ("input_steeringPercent", ctypes.c_float),

        # Position
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("posZ", ctypes.c_float),

        # Velocity
        ("velX", ctypes.c_float),
        ("velY", ctypes.c_float),
        ("velZ", ctypes.c_float),

        # Acceleration
        ("accX", ctypes.c_float),
        ("accY", ctypes.c_float),
        ("accZ", ctypes.c_float),

        # Up vector
        ("upVecX", ctypes.c_float),
        ("upVecY", ctypes.c_float),
        ("upVecZ", ctypes.c_float),

        # Forward vector
        ("forwardVecX", ctypes.c_float),
        ("forwardVecY", ctypes.c_float),
        ("forwardVecZ", ctypes.c_float),

        # Orientation
        ("rollPos", ctypes.c_float),
        ("pitchPos", ctypes.c_float),
        ("yawPos", ctypes.c_float),

        ("rollRate", ctypes.c_float),
        ("pitchRate", ctypes.c_float),
        ("yawRate", ctypes.c_float),

        ("rollAcc", ctypes.c_float),
        ("pitchAcc", ctypes.c_float),
        ("yawAcc", ctypes.c_float),

        # Suspension
        ("suspension_position_fl", ctypes.c_float),
        ("suspension_position_fr", ctypes.c_float),
        ("suspension_position_rl", ctypes.c_float),
        ("suspension_position_rr", ctypes.c_float),

        ("suspension_velocity_fl", ctypes.c_float),
        ("suspension_velocity_fr", ctypes.c_float),
        ("suspension_velocity_rl", ctypes.c_float),
        ("suspension_velocity_rr", ctypes.c_float),

        ("suspension_acceleration_fl", ctypes.c_float),
        ("suspension_acceleration_fr", ctypes.c_float),
        ("suspension_acceleration_rl", ctypes.c_float),
        ("suspension_acceleration_rr", ctypes.c_float),

        # Wheels
        ("wheel_slip_fl", ctypes.c_float),
        ("wheel_slip_fr", ctypes.c_float),
        ("wheel_slip_rl", ctypes.c_float),
        ("wheel_slip_rr", ctypes.c_float),

        ("wheel_RPS_fl", ctypes.c_float),
        ("wheel_RPS_fr", ctypes.c_float),
        ("wheel_RPS_rl", ctypes.c_float),
        ("wheel_RPS_rr", ctypes.c_float),

        ("wheel_speed_fl", ctypes.c_float),
        ("wheel_speed_fr", ctypes.c_float),
        ("wheel_speed_rl", ctypes.c_float),
        ("wheel_speed_rr", ctypes.c_float),

        ("wheel_isRubberTire_fl", ctypes.c_int32),
        ("wheel_isRubberTire_fr", ctypes.c_int32),
        ("wheel_isRubberTire_rl", ctypes.c_int32),
        ("wheel_isRubberTire_rr", ctypes.c_int32),

        ("wheel_contactMaterial_fl", ctypes.c_int32),
        ("wheel_contactMaterial_fr", ctypes.c_int32),
        ("wheel_contactMaterial_rl", ctypes.c_int32),
        ("wheel_contactMaterial_rr", ctypes.c_int32),

        ("wheel_isDeflated_fl", ctypes.c_int32),
        ("wheel_isDeflated_fr", ctypes.c_int32),
        ("wheel_isDeflated_rl", ctypes.c_int32),
        ("wheel_isDeflated_rr", ctypes.c_int32),

        ("wheel_contactDepth_fl", ctypes.c_float),
        ("wheel_contactDepth_fr", ctypes.c_float),
        ("wheel_contactDepth_rl", ctypes.c_float),
        ("wheel_contactDepth_rr", ctypes.c_float),

        ("brake_surfaceTemperature_fl", ctypes.c_float),
        ("brake_surfaceTemperature_fr", ctypes.c_float),
        ("brake_surfaceTemperature_rl", ctypes.c_float),
        ("brake_surfaceTemperature_rr", ctypes.c_float),

        ("brake_coreTemperature_fl", ctypes.c_float),
        ("brake_coreTemperature_fr", ctypes.c_float),
        ("brake_coreTemperature_rl", ctypes.c_float),
        ("brake_coreTemperature_rr", ctypes.c_float),

        ("check", ctypes.c_int32),

        ("reserved_1", ctypes.c_float),
        ("reserved_2", ctypes.c_float),
        ("reserved_3", ctypes.c_float),
        ("reserved_4", ctypes.c_float),
    ]

class SimplifiedTelemetryPacket(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("idle_rpm", ctypes.c_float),
        ("max_rpm", ctypes.c_float),

        ("gear", ctypes.c_int32),
        ("max_gears", ctypes.c_int32),
        ("rpm", ctypes.c_float),
        ("turbo", ctypes.c_float),
        ("turboMax", ctypes.c_float),

        ("input_throttle", ctypes.c_float),
        ("input_brake", ctypes.c_float),
        ("input_clutch", ctypes.c_float),
        ("input_parkingBrake", ctypes.c_float),
        ("input_steeringPercent", ctypes.c_float),

        ("accY", ctypes.c_float),
        ("pitchPos", ctypes.c_float),

        ("wheel_speed_fl", ctypes.c_float),
        ("wheel_speed_fr", ctypes.c_float),
        ("wheel_speed_rl", ctypes.c_float),
        ("wheel_speed_rr", ctypes.c_float),

        ("suspension_position_fl", ctypes.c_float),
        ("suspension_position_fr", ctypes.c_float),
        ("suspension_position_rl", ctypes.c_float),
        ("suspension_position_rr", ctypes.c_float),
    ]

def convert_to_simplified(full_packet):
    """Convert a full TelemetryPacket to a SimplifiedTelemetryPacket."""
    simplified = SimplifiedTelemetryPacket()
    simplified.idle_rpm = full_packet.idle_rpm
    simplified.max_rpm = full_packet.max_rpm
    simplified.gear = full_packet.gear - 1 # 0 is reverse, 1 is neutral, 2 is first gear
    simplified.max_gears = full_packet.max_gears
    simplified.rpm = full_packet.rpm
    simplified.turbo = full_packet.turbo * 14.505  # Convert bar to psi
    simplified.turboMax = full_packet.turboMax * 14.505  # Convert bar to psi
    simplified.input_throttle = full_packet.input_throttle
    simplified.input_brake = full_packet.input_brake
    simplified.input_clutch = full_packet.input_clutch
    simplified.input_parkingBrake = full_packet.input_parkingBrake
    simplified.input_steeringPercent = full_packet.input_steeringPercent
    simplified.accY = full_packet.accY / 9.81  # Normalize to g-force
    simplified.pitchPos = (full_packet.pitchPos * (180.0 / 3.14159265))  # Convert radians to degrees
    simplified.wheel_speed_fl = full_packet.wheel_speed_fl * 2.23694  # Convert m/s to mph
    simplified.wheel_speed_fr = full_packet.wheel_speed_fr * 2.23694  # Convert m/s to mph
    simplified.wheel_speed_rl = full_packet.wheel_speed_rl * 2.23694  # Convert m/s to mph
    simplified.wheel_speed_rr = full_packet.wheel_speed_rr * 2.23694  # Convert m/s to mph
    simplified.suspension_position_fl = full_packet.suspension_position_fl
    simplified.suspension_position_fr = full_packet.suspension_position_fr
    simplified.suspension_position_rl = full_packet.suspension_position_rl
    simplified.suspension_position_rr = full_packet.suspension_position_rr
    return simplified

def noprint_shift(data, num_bytes):
    """Return the remaining data shifted by num_bytes without printing."""
    return data[num_bytes:]

def parse_telemetry_packet(contents):

    is_binary = isinstance(contents, bytes)

    if is_binary:
        content_byte = contents
    else:
        content_byte = bytes.fromhex(contents)
   
    while content_byte[:1] != b'm':
        content_byte = noprint_shift(content_byte, 1)

    packet_size = ctypes.sizeof(TelemetryPacket)
    if len(content_byte) < packet_size:
        print("Insufficient data for a complete TelemetryPacket.")
        return
    
    packet = TelemetryPacket.from_buffer_copy(content_byte[:packet_size])

    if packet.check == 128:
        return convert_to_simplified(packet)
    else:
        print("Invalid packet check value.")
    return

def send_headers():
    headers = [field[0] for field in SimplifiedTelemetryPacket._fields_]
    return headers

