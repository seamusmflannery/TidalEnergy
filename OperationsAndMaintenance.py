# Author: Seamus Flannery
# Used for Q9
import csv


# reads data from CSV
def read_data(file_name):
    with open(file_name, newline='') as file:
        data_array = [list(map(float, row)) for row in csv.reader(file)]
        flipped_data = list(
            map(list, zip(*data_array)))  # from https://stackoverflow.com/questions/6473679/transpose-list-of-lists
        return flipped_data


# sensor check requires 20 mins, but each time slot is 30 mins so no need to check duration
# considers a window longer than one slot to be just a single opportunity
def sensor_check_opportunity(in_data):
    [times, uref, power, waves] = in_data
    opportunities = 0
    concurrency_flag = False
    for i, time in enumerate(times):
        if 1 > uref[i] > -1 and waves[i] < 0.5:
            if not concurrency_flag:
                opportunities += 1
                concurrency_flag = True
        else:
            concurrency_flag = False
    return opportunities


# long-duration repair also checks if a window of acceptable conditions lasts for 24 consecutive 30 minute slots
# considers a window longer than 24 slots to be just a single opportunity.
def repair_opportunity(in_data):
    [times, uref, power, waves] = in_data
    opportunities = 0
    consecutive = 0
    concurrency_flag = False
    consecutive_flag = False
    for i, time in enumerate(times):
        if 1.75 > uref[i] > -1.75 and waves[i] < 1.5:
            if concurrency_flag:
                consecutive += 1
            else:
                consecutive = 1
                concurrency_flag = True
            if consecutive >= 24 and not consecutive_flag:
                opportunities += 1
                consecutive_flag = True
        else:
            concurrency_flag = False
            consecutive_flag = False
            consecutive = 0
    return opportunities


if __name__ == '__main__':
    data = read_data("Threasholding.csv")
    print(data)
    print("sensor check opportunities: " + str(sensor_check_opportunity(data)))
    print("long-duration repair opportunities: " + str(repair_opportunity(data)))
