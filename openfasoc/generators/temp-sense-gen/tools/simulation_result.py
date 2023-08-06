import re
import sys
import math

def get_value(log_file_text, key):
    """Finds a value in the simulation log file.

    Finds and returns the value from a statement of the format key = value.
    """
    pattern = f"{key}\s*=\s*([0-9\.e-]+)"
    pattern_re = re.search(pattern, log_file_text, flags=re.IGNORECASE)
    value = "failed"

    if pattern_re:
        value = pattern_re.group(1)

    return value

def get_sim_results(log_file_text):
    temp_value = get_value(log_file_text=log_file_text, key="temp")
    period_value = get_value(log_file_text=log_file_text, key="period")
    power_value = get_value(log_file_text=log_file_text, key="power")

    return {
        'temp': temp_value,
        'period': period_value,
        'power': power_value
    }

def calculate_sim_error(sim_output_lines: list[str]):
    temp_list = []
    period_list = []
    power_list = []

    for line in sim_output_lines:
        data = line.split()
        temp_list.append(float(data[0]))
        period_list.append(float(data[1]))
        power_list.append(float(data[2]))

    frequency_list = []
    data1 = []

    for i, x in enumerate(period_list):
        if x == "failed":
            x = "failed"
            frequency = "failed"
        else:
            frequency = 1 / float(x)
            print("temp: %f, \tfrequency: %f" % (temp_list[i], frequency))

            x = math.log(1 / float(x)) * (temp_list[i] + 273.15) * 0.01

        frequency_list.append(frequency)
        data1.append(x)

    try:
        slope_f = (temp_list[-2] - temp_list[1]) / (data1[-2] - data1[1])
    except:
        print("Error calculation failed")
        sys.exit(1)

    data2 = []
    for data in data1:
        if data == "failed":
            x = "failed"
        else:
            x = data * slope_f
        data2.append(x)

    data3 = []
    offset = data2[0] - temp_list[0]
    for val in data2:
        if val == "failed":
            val = "failed"
        else:
            val = val - offset
        data3.append(val)

    error_list = []
    for i, x in enumerate(data3):
        if x == "failed":
            error = "failed"
        else:
            error = temp_list[i] - x
        error_list.append(error)

    error_data: list[str] = []
    error_data.append("Temp Frequency Power Error")
    for idx, temp in enumerate(temp_list):
        error_data.append(f"{temp} {frequency_list[idx]} {power_list[idx]} {error_list[idx]}")

    return error_data
