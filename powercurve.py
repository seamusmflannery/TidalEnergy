# Author: Seamus Flannery
# importable code to handle power curve calculations, fitting, and imports
# csv reader template from https://stackoverflow.com/questions/49312300/read-csv-to-float-array
import csv
import numpy as np
import scipy
import matplotlib.pyplot as plt


def read_data(file_name):
    with open(file_name, newline='') as file:
        csvreader = csv.reader(file)
        out_array = []
        for row in csvreader:
            out_array.append(row)
        out_array.pop(0)
        out_array = [list(map(float, point)) for point in out_array]
        return out_array


def logistic_curve(x, a, b, c, d):
    return a/(1. + np.exp(-c * (x-d))) + b


def function_fit(data, plotter=True):
    x_vals = [x for x, y in data]
    y_vals = [y for x, y in data]
    b = y_vals[1]  # cut-in power
    a = max(y_vals) - b
    cut_in_v = x_vals[1]  # cut-in velocity
    if plotter:
        plt.plot(x_vals, y_vals, label="Measured Powercurve", linestyle="", marker="o", markersize="3")
    c_, d_ = scipy.optimize.curve_fit(lambda x, c, d: logistic_curve(x, a, b, c, d), x_vals, y_vals,
                                      [max(x_vals)*2/3, 2])[0]
    if plotter:
        fit_space = np.linspace(x_vals[0], x_vals[len(x_vals)-1])
        y_fit = logistic_curve(fit_space, a, b, c_, d_)
        plt.plot(fit_space, y_fit, label="Powercurve Fit")
        plt.axvline(cut_in_v, label="Cut-In Velocity (" + str(cut_in_v) + " m/s)", color="green")
        plt.legend()
        plt.title("Powercurve and Powercurve Fit")
        plt.xlabel("Flow Velocity (m/s)")
        plt.ylabel("Power (kW)")
        print("a= " + str(a))
        print("b= " + str(b))
        print("c= " + str(c_))
        print("d= " + str(d_))
        print("cut-in v = " + str(cut_in_v))
        plt.show()
    return a, b, c_, d_, cut_in_v


if __name__ == '__main__':
    powercurve_16 = read_data("16M_Powercurve.csv")
    powercurve_20 = read_data("20M_Powercurve.csv")
    a_16, b_16, c_16, d_16, cut_in_v_16 = function_fit(powercurve_16)
    a_20, b_20, c_20, d_20, cut_in_v_20 = function_fit(powercurve_20)
