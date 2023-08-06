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
        temp_list.append(data[0])
        period_list.append(data[1])
        power_list.append(data[2])

    frequency_list = []
    calculated_temp_list = []

    for i, calculated_temp in enumerate(period_list):
        if calculated_temp == "failed":
            cal_temp = "failed"
            frequency = "failed"
        else:
            frequency = 1 / float(calculated_temp)
            print("temp: %s, \tfrequency: %f" % (temp_list[i], frequency))

            cal_temp = math.log(1 / float(calculated_temp)) * ((-20 + i * 20) + 273.15) * 0.01

        frequency_list.append(frequency)
        calculated_temp_list.append(cal_temp)

    try:
        slope_f = (temp_list[-2] - temp_list[1]) / (calculated_temp_list[-2] - calculated_temp_list[1])
    except:
        print("Error calculation failed")
        sys.exit(1)

    data2 = []
    for temp in calculated_temp_list:
        if temp == "failed":
            calculated_temp = "failed"
        else:
            calculated_temp = temp * slope_f
        data2.append(calculated_temp)

    error_list = []
    error_list.append("Temp Frequency Power Error")
    for i, calculated_temp in enumerate(data2):
        if calculated_temp == "failed":
            error = "failed"
        else:
            error = (temp_list[i]) - calculated_temp
        error_list.append(error)

    error_data: list[str] = []
    for idx, temp in enumerate(temp_list):
        error_data.append("%s %s %s %s" % (temp, frequency_list[idx], power_list[idx], error_list[idx]))

    return error_data
