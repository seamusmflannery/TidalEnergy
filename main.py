# Author: Seamus Flannery
# Reads East and North Component data from CSV files, calculates power and energy output
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt
import powercurve


# csv reader template from https://stackoverflow.com/questions/49312300/read-csv-to-float-array
def read_data(file_name):
    with open(file_name, newline='') as file:
        return [list(map(float, row)) for row in csv.reader(file)]


# This method combines north and east data into one table giving flow magnitude at 10 minute samples (row)
# and at different depth cells (column)
def v_magnitudes(east_data, north_data):
    magnitude_data = np.zeros((len(east_data), len(east_data[0])), float)
    for i in range(len(east_data)):
        for j in range(len(east_data[0])):
            magnitude_data[i, j] = (east_data[i][j] ** 2 + north_data[i][j] ** 2) ** (1 / 2)
    return magnitude_data


# takes velocity data and transforms to power data in kWh
def v_to_p(velocity_data, rotor_data):
    p_data = np.zeros((len(velocity_data), len(velocity_data[0])), float)
    powercurve_data = powercurve.read_data(rotor_data)
    a, b, c, d, cut_in_v = powercurve.function_fit(powercurve_data, plotter=False)
    for i, row in enumerate(velocity_data):
        for j, velocity in enumerate(row):
            if velocity > cut_in_v:
                power = powercurve.logistic_curve(velocity, a, b, c, d)
            else:
                power = 0
            p_data[i][j] = power
    return p_data


# Integrates over a section of a circle, from the bottom up, in 1 meter tall horizontal cells
def rect_circle_section(radius, y_low_lim, y_up_lim):
    return abs(scipy.integrate.quad(lambda x: -2 * np.sqrt(radius ** 2 - x ** 2),
                                    y_low_lim - radius, y_up_lim - radius)[0]) / (np.pi * radius ** 2)


# uses the power data and the rotor characteristics to calculate the PowerWeightedRotorAverage (PWRA)
# POSSIBLY ONLY WORKS FOR ROTORS WITH EVEN DIAMETERS
# Uses heights from seabed from reference, rather than depths. Hard Coded to 1m tall horizontal cells
def pwra(power_data, hub_height, rotor_diameter):
    print("Calculating PWRA step for " + str(rotor_diameter) + "m dia. rotor, with hub height " + str(
        hub_height) + "m...")
    power_array = np.zeros((len(power_data)), float)
    radius = rotor_diameter / 2
    bottom_height = hub_height - radius
    for date_time in range(len(power_data)):
        for height in range(rotor_diameter):
            section_area = rect_circle_section(radius, height, height + 1)
            section_power = power_data[date_time, int(bottom_height + height)] * section_area
            power_array[date_time] += section_power
    return power_array


# given power array returns total energy over sample period. Sample rate in hours (1/6 = 10 minutes)
def get_total_e(power_array, sample_rate=1 / 6):
    return sum(power_array) * sample_rate


def calc_capacity_factor(actual_yield, rotor_powercurve, v_data, data_sample_rate=1 / 6):
    max_rated_power = max(max(powercurve.read_data(rotor_powercurve)))
    duration = len(v_data) * data_sample_rate
    capacity_factor = actual_yield / (max_rated_power * duration)
    return capacity_factor


def plot_flow_speed(v_data):
    avg_v = np.empty((len(v_data)))
    for i, row in enumerate(v_data):
        avg_v[i] = np.average(row)
    plt.plot(range(0, len(v_data)), avg_v)
    plt.title("Average Flow Speed (Not Velocity) Through The Channel Vs. Time")
    plt.xlabel("Time since 17/9/14, 7:00 (10's of minutes)")
    plt.ylabel("Water Flow Speed (m/s)")
    plt.show()
    return True


def plot_days_flow(v_data):
    avg_v = np.empty((len(v_data)))
    for i, row in enumerate(v_data):
        avg_v[i] = np.average(row)
    daily_max = np.empty(int(len(avg_v) / 144) - 1)
    for i in range(int(len(avg_v) / 144) - 1):
        daily_max[i] = max(avg_v[i*144:(i+1)*144])
    plt.plot(range(0, len(daily_max)), daily_max)
    plt.title("Daily Maximum Average Flow Speed Through The Channel Vs. Time")
    plt.xlabel("Time since 17/9/14, 7:00 (Days)")
    plt.ylabel("Water Flow Speed (m/s)")
    plt.show()
    return True



if __name__ == '__main__':
    # Q5
    # Read in velocity component data
    EastData = read_data("EastDataCleaned.csv")
    NorthData = read_data("NorthDataCleaned.csv")
    # combine velocity components to get magnitudes
    VMagData = v_magnitudes(EastData, NorthData)
    # convert velocity magnitude to power for 20m rotor and 16m rotor
    PData_20 = v_to_p(VMagData, "20M_Powercurve.csv")
    PWR_Array_20 = pwra(PData_20, 15, 20)
    PData_16 = v_to_p(VMagData, "16M_Powercurve.csv")
    PWR_Array_16 = pwra(PData_16, 20, 16)
    # plot the power vs. time - note the three months of tidal differences (two cycles of max power per month)
    # plt.figure(1)
    # plt.plot(range(0, len(PWR_Array_20)), PWR_Array_20)
    # plt.title("20m Rotor Power")
    # plt.xlabel("10's of Minutes")
    # plt.ylabel("Power (kW)")
    # plt.figure(2)
    # plt.plot(range(0, len(PWR_Array_16)), PWR_Array_16)
    # plt.title("16m Rotor Power")
    # plt.xlabel("10's of Minutes")
    # plt.ylabel("Power (kW)")
    # plt.show()
    # calculate total energy yields
    total_E20 = get_total_e(PWR_Array_20)
    print("Total E yield for 20m rotor over 3 months is: ")
    print(str(total_E20) + "kWh")
    total_E16 = get_total_e(PWR_Array_16)
    print("Total E yield over for 16m rotor over 3 months is: ")
    print(str(total_E16) + "kWh")
    # Q6
    # calculate capacity factor
    cap_fact_20 = calc_capacity_factor(total_E20, "20M_Powercurve.csv", VMagData)
    cap_fact_16 = calc_capacity_factor(total_E16, "16M_Powercurve.csv", VMagData)
    print("Cap Factor 20m Rotor is: " + str(cap_fact_20))
    print("Cap Factor 16m Rotor is: " + str(cap_fact_16))
    # Q8
    # plot flow over the entire measurement period
    # plot_flow_speed(VMagData)
    # plot flow over just one day (144 tens of minutes)
    # plot_flow_speed(VMagData[0:144])
    # plot_flow_speed(VMagData[0:(144*4)])
    plot_days_flow(VMagData)
