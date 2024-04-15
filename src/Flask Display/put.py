import csv
from datetime import datetime, timedelta
import random
import time
import copy

n_data = 0

while True:

    if n_data == 0:
        with open('out.csv', 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)
    n_data = copy.deepcopy(data[-1])
    print(n_data)
    for k, v in n_data.items():
        try:
            cell_val = float(v)
            n_data[k] = str(cell_val + random.uniform(-5, 5))
        except ValueError:
            pass
        except TypeError:
            pass
    val_time = datetime.strptime(n_data['Time'], '%H:%M:%S.%f')
    val_time = val_time + timedelta(seconds=random.uniform(20, 80))
    n_data['Time'] = val_time.strftime('%H:%M:%S.%f')
    fieldnames = csv_reader.fieldnames
    #print(data)
    data.append(n_data)
    with open('out.csv', 'w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    time.sleep(5)