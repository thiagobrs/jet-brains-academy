# imports the necessary packages
import json
import re
from datetime import datetime


# function that validates the date
def is_valid_date(date_str):
    # checks if it was given in the correct data type
    if type(date_str) != str:
        return False
    # as it is a required field, checks if it was informed
    elif len(date_str) < 5:
        return False
    # checks if it was informed in the correct format
    elif (not date_str[:2].isdigit()) or \
         (date_str[2] != ':') or \
         (not date_str[3:].isdigit()):
        return False
    # checks if it is a valid time
    elif (date_str[0] not in ['0', '1', '2']) or \
         (date_str[3] not in ['0', '1', '2', '3', '4', '5']):
        print(date_str[0])
        print(date_str[3])
        return False
    else:
        return True


# function that validates field types and required fields
def validate_fields(data):
    # error variables
    total_err, bus_id_err, stop_id_err, stop_name_err, next_stop_err, stop_type_err, a_time_err = 0, 0, 0, 0, 0, 0, 0

    # iterates over each json sub-element
    for bus_line in data:
        # checks data types and required fields
        if type(bus_line["bus_id"]) != int:
            bus_id_err += 1
            total_err += 1
        if type(bus_line["stop_id"]) != int:
            stop_id_err += 1
            total_err += 1
        if (type(bus_line["stop_name"]) != str) or (bus_line["stop_name"].strip() == ''):
            stop_name_err += 1
            total_err += 1
        if type(bus_line["next_stop"]) != int:
            next_stop_err += 1
            total_err += 1
        if (type(bus_line["stop_type"]) != str) or (bus_line["stop_type"] not in ['', 'S', 'O', 'F']):
            stop_type_err += 1
            total_err += 1
        if not is_valid_date(bus_line["a_time"]):
            a_time_err += 1
            total_err += 1

    # prints the errors found
    print(f"Type and required field validation: {total_err} errors")
    print(f"bus_id: {bus_id_err}")
    print(f"stop_id: {stop_id_err}")
    print(f"stop_name: {stop_name_err}")
    print(f"next_stop: {next_stop_err}")
    print(f"stop_type: {stop_type_err}")
    print(f"a_time: {a_time_err}")


# function that validates stop name, stop type and time formats
def validate_fields_regex(data):
    # error variables
    total_err, stop_name_err, stop_type_err, a_time_err = 0, 0, 0, 0

    # iterates over each json sub-element
    for bus_line in data:
        # checks data types and required fields
        template = r"^([A-Z]\w+\s)+(Road|Avenue|Boulevard|Street)$"
        if not re.match(template, bus_line["stop_name"]):
            stop_name_err += 1
            total_err += 1
        if bus_line["stop_type"] not in ['', 'S', 'O', 'F']:
            stop_type_err += 1
            total_err += 1
        template = "^([0-1][0-9]|2[0-3]):([0-5][0-9])$"
        if not re.match(template, bus_line["a_time"]):
            a_time_err += 1
            total_err += 1

    # prints the missing and type errors found
    print(f"Format validation: {total_err} errors")
    print(f"stop_name: {stop_name_err}")
    print(f"stop_type: {stop_type_err}")
    print(f"a_time: {a_time_err}")


# function that retrieve bus lines name and number of stops
def get_bus_line_info(data):
    # dictionary to store bus lines and number of stops
    bus_line_dict = {}

    # iterates over each json sub-element
    for bus_line in data:
        # creates or updates the bus_id and the number of stops in the dictionary
        bus_line_dict[bus_line["bus_id"]] = bus_line_dict.get(bus_line["bus_id"], 0) + 1

    # prints the lines and the number of stops
    print("Line names and number of stops:")
    for bus_line, stops in bus_line_dict.items():
        print(f"bus_id: {bus_line}, stops: {stops}")


# function that validate if every bus line has one start stop and one finish stop
def validate_start_stop(data):
    flag_ok = True

    # dictionary to store bus lines and number of starting point, final stops and transfer stops
    starting_point_dict, final_stop_dict, transfer_stop_dict = dict(), dict(), dict()

    # sets of starting point, final stops and transfer stops
    starting_point_set, final_stop_set, transfer_stop_set = set(), set(), set()

    # iterate over each json sub-element
    for bus_line in data:
        # gets the actual bus_id
        actual_bus_id = str(bus_line["bus_id"])

        # updates the dictionaries with this bus line information
        starting_point_dict[actual_bus_id] = starting_point_dict.get(actual_bus_id, 0)
        final_stop_dict[actual_bus_id] = final_stop_dict.get(actual_bus_id, 0)
        transfer_stop_dict[bus_line["stop_name"]] = transfer_stop_dict.get(bus_line["stop_name"], 0) + 1

        # if this stop_name has more than 1 occurrence, it means that it is shared by 2 or more bus lines
        # so, we add it to the transfer_set
        if transfer_stop_dict.get(bus_line["stop_name"], 0) > 1:
            transfer_stop_set.add(bus_line["stop_name"])

        # if it is a starting point...
        if bus_line["stop_type"] == "S":
            # check if another starting point has already been detected for this line
            if starting_point_dict.get(actual_bus_id, 0) > 0:
                print(f'There is more than one starting point for the line: {actual_bus_id}.')
                flag_ok = False
                break
            else:
                # if not, indicate that one starting point was detected for this line
                starting_point_dict[actual_bus_id] = 1

                # add this starting point to the starting_point_set
                starting_point_set.add(bus_line["stop_name"])

        # if it is a final stop...
        elif bus_line["stop_type"] == "F":
            # check if another final stop has already been detected for this line
            if final_stop_dict.get(actual_bus_id, 0) > 0:
                print(f'There is more than one final stop for the line: {actual_bus_id}.')
                flag_ok = False
                break
            else:
                # if not, indicate that one starting point was detected for this line
                final_stop_dict[actual_bus_id] = 1

                # add this final stop to the final_stop_set
                final_stop_set.add(bus_line["stop_name"])

    # if everything is ok until this point...
    if flag_ok:
        # check if every bus line has a starting point and a final stop
        for key in sorted(starting_point_dict):
            if starting_point_dict[key] + final_stop_dict[key] < 2:
                print(f'There is no start or end stop for the line: {key}.')
                flag_ok = False

    # if everything is still ok...
    if flag_ok:
        # print the stop types info
        print(f"Start stops: {len(starting_point_set)} {sorted(starting_point_set)}")
        print(f"Transfer stops: {len(transfer_stop_set)} {sorted(transfer_stop_set)}")
        print(f"Finish stops: {len(final_stop_set)} {sorted(final_stop_set)}")


# function tha validate the arrival times
def validate_arrival_time(data):
    print("Arrival time test:")

    previous_bus_id = -1
    previous_a_time = ""
    result = True

    # this flag indicates that the current bus_id shall not be tested anymore
    flag_skip_bus_id = False

    # iterate over each json sub-element
    for bus_line in data:
        if flag_skip_bus_id and (previous_bus_id == bus_line["bus_id"]):
            continue

        # if it is the first stop of the bus line, there is no previous a_time to compare with
        if bus_line["stop_type"] == "S":
            # so, just store the bus_id and a_time to compare with the next stop
            previous_bus_id = bus_line["bus_id"]
            previous_a_time = datetime.strptime(bus_line["a_time"], "%H:%M")

            # set the flags to False, so this if clause will not be executed again for this bus line
            flag_skip_bus_id = False
        else:
            # get the a_time for the current stop_id
            current_a_time = datetime.strptime(bus_line["a_time"], "%H:%M")

            # if the current stop is inconsistent with the previous one, print a message
            if current_a_time <= previous_a_time:
                print(f"bus_id line {str(bus_line['bus_id'])}: wrong time on station {bus_line['stop_name']}")

                # indicate that the validation of this bus_id is over and an error occurred
                result = False
                flag_skip_bus_id = True
            else:
                # the actual bus_line becomes the previous
                previous_bus_id = bus_line['bus_id']
                previous_a_time = current_a_time

    if result:
        print("OK")


# function that gets all the special stops: start, transfer, finish or on-demand
def get_special_stops(data):
    # dictionary to identify transfer stops
    transfer_stop_dict = dict()

    # sets of starting point, final stops and transfer stops
    starting_point_set, final_stop_set, transfer_stop_set, ondemand_stop_set = set(), set(), set(), set()

    # iterate over each json sub-element
    for bus_line in data:
        # update the transfer stop dictionary with this bus line information
        transfer_stop_dict[bus_line["stop_name"]] = transfer_stop_dict.get(bus_line["stop_name"], 0) + 1

        # if this stop_name has more than 1 occurrence, it means that it is shared by 2 or more bus lines
        # so, we add it to the transfer_set
        if transfer_stop_dict.get(bus_line["stop_name"], 0) > 1:
            transfer_stop_set.add(bus_line["stop_name"])

        # check if it is a special stop and update the appropriate set
        if bus_line["stop_type"] == "S":
            # add this starting point to the starting_point_set
            starting_point_set.add(bus_line["stop_name"])
        elif bus_line["stop_type"] == "F":
            # add this final stop to the final_stop_set
            final_stop_set.add(bus_line["stop_name"])
        elif bus_line["stop_type"] == "O":
            # add this on-demand stop to the on_demand_set
            ondemand_stop_set.add(bus_line["stop_name"])

    return starting_point_set, final_stop_set, transfer_stop_set, ondemand_stop_set


def on_demand_stop_test(data):
    print("On demand stops test:")

    # get all the special stops
    starting_set, final_set, transfer_set, ondemand_set = get_special_stops(data)

    # make the union of all special stops sets
    special_stops = starting_set.union(final_set, transfer_set)

    # intersect the special stops sets with the on-demand set
    ondemand_special = sorted(ondemand_set.intersection(special_stops))

    # print the appropriate message
    print(f"Wrong stop type: {ondemand_special}" if len(ondemand_special) > 0 else print("OK"))


def main():
    # converts the input json string
    data_example_json = json.loads(input())

    validate_fields(data_example_json)
    validate_fields_regex(data_example_json)
    get_bus_line_info(data_example_json)
    validate_start_stop(data_example_json)
    validate_arrival_time(data_example_json)
    on_demand_stop_test(data_example_json)


if __name__ == "__main__":
    main()
