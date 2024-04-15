from datetime import datetime
import time
import csv
import os


def print_results(unique_row_counter, duplicate_rows, bad_rows, trash_rows, total_row_count):

    print('\n')
    print('New and Clean Rows: ', unique_row_counter)
    print('Duplicate Rows: ', duplicate_rows)
    print('Bad Rows (Number): ', bad_rows)
    print('Trash Rows: ', trash_rows)
    print('Total_Row_Count: ', total_row_count)
    print('Uniq/Dup/Bad/Trash: ', unique_row_counter + duplicate_rows + bad_rows + trash_rows)
    if (total_row_count == (unique_row_counter + duplicate_rows + bad_rows + trash_rows)):
        print('All the Numbers Match!')


def is_file_empty(file_path):
    return not os.path.exists(file_path) or os.stat(file_path).st_size == 0


def reset_last_position(last_position_file):
    # Reset the last read position to the start of the file
    with open(last_position_file, 'w') as pos_file:
        pos_file.write('0')


def clean_row(entry):

    trash = ['Date', 'ate', 'Time','psi','temperature','altitude','CO2level','relativeHumidity','scdTemperature','bmp_temperature','bmp_pressu', 'bmp_pressure']
    for k in range(0, len(entry)):
        if entry[k] in trash:
            return 'Bad Entry'
    return entry


def parse_new_entries(input_csv_path, output_csv_path, last_position_file, unique_entries, already_written):

    # Read the last read position
    with open(last_position_file, 'r') as pos_file:
        last_position = int(pos_file.read().strip())

    # Read new entries from the input CSV starting from the last read position
    with open(input_csv_path, 'r', newline='') as input_file:

        input_file.seek(last_position)

        total_row_count = 0
        duplicate_rows = 0
        trash_rows = 0
        bad_rows = 0
        unique_row_counter = 0

        csv_reader = csv.reader(input_file)

        for row in csv_reader:

            total_row_count += 1

            if ((len(row) < 15) or (len(row) > 15)):
                trash_rows += 1
                continue

            row = clean_row(row)
            if row == "Bad Entry":
                bad_rows += 1
                continue
            else:
                time_stamp = row[1].strip()
                if time_stamp in unique_entries:
                    duplicate_rows += 1
                    continue
                else:
                    print('unique time_stamp: ', time_stamp)
                    unique_row_counter += 1
                    unique_entries[time_stamp] = row

        print_results(unique_row_counter, duplicate_rows, bad_rows, trash_rows, total_row_count)

        # Remember the position where we stop reading
        new_position = input_file.tell()

    # Append unique new entries to the output CSV
    with open(output_csv_path, 'a', newline='') as output_file:

        csv_writer = csv.writer(output_file)
        sorted_data = sorted(list(unique_entries.values()), key=lambda x: datetime.strptime(f"{x[0]} {x[1]}", '%Y-%m-%d %H:%M:%S.%f'))

        for entry in sorted_data:
            if entry in already_written:
                continue
            else:
                csv_writer.writerow(entry)
                already_written.append(entry)

    # Update the last read position
    with open(last_position_file, 'w') as pos_file:
        pos_file.write(str(new_position))

    return unique_entries, already_written



def clean_data():

    unique_entries = {}
    already_written = []

    # File paths
    input_csv_path = 'output_csv.csv'
    output_csv_path = 'out.csv'

    os.remove(output_csv_path)

    last_position_file = 'last_read_position.txt'
    
    # Reset the last read position on startup
    reset_last_position(last_position_file)

    # Only write headers if the file is empty or does not exist
    if is_file_empty(output_csv_path):
        with open(output_csv_path, 'w', newline='') as output_file:  # Use 'w' mode to write
            csv_writer = csv.writer(output_file)
            headers = ['Date', 'Time', 'psi', 'temperature', 'altitude', 'CO2level', 'relativeHumidity', 'scdTemperature', 'bmp_temperature', 'bmp_pressure', 'bmp_altitude', 'duration', 'uSvh', 'uSvhError', 'cpm']
            csv_writer.writerow(headers)

    ## Continuously parse new entries and update the output CSV
    while True:
        unique_entries, already_written = parse_new_entries(input_csv_path, output_csv_path, last_position_file, unique_entries, already_written)
        time.sleep(4)


clean_data()
