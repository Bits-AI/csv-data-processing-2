import csv
from datetime import datetime, timedelta
import os

def file_process(filename):
    with open(f"./Output/Processed_{filename}", "w", newline="") as csv_write:
        writer = csv.writer(csv_write)

        with open(f"./Source/{filename}") as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 1

            for row in csv_reader:
                if line_count < 16:
                    writer.writerow(row)

                elif (line_count == 16):
                    writer.writerow(['Date', 'Time', 'Event Start Date', 'Event Start Time', 'Maximum'])

                else:
                    timestamp = row[0].split(" ")
                    event_timestamp = row[1].split(" ")

                    #Convert the date section to date object first
                    date = format_date(timestamp[0])
                    event_date = format_date(event_timestamp[0])

                    new_date, new_time = format_timestamp(date, timestamp[1])
                    new_event_date, new_event_time = format_timestamp(event_date, event_timestamp[1])

                    value = format_value(row[2])

                    writer.writerow([new_date, new_time, new_event_date, new_event_time, value])

                print(f"Processed {line_count} in file.\r", end="")

                line_count += 1

def format_date(date_raw):
    #Convert the date section to date object first
    try:
        date = datetime.strptime(date_raw, "%Y/%m/%d")

    except ValueError:
        try:
            date = datetime.strptime(date_raw, "%Y-%m-%d")

        except ValueError:
            try:
                date = datetime.strptime(date_raw, "%d/%m/%Y")

            except ValueError:
                date = datetime.strptime(date_raw, "%d-%m-%Y")

    finally:
        return date

def format_timestamp(date, time):
    #Check the time if it is equals to 12am midnight
    if (time == "0:00"):
        date_calc = date - timedelta(days=1)
        new_date = datetime.strftime(date_calc, "%d-%m-%Y")
        # new_time = "24:00"
        new_time = "23:59:59"

    elif (time == "00:00:00"):
        date_calc = date - timedelta(days=1)
        new_date = datetime.strftime(date_calc, "%d-%m-%y")
        # new_time = "24:00"
        new_time = "23:59:59"

    else:
        try:
            new_date = datetime.strftime(date, "%d-%m-%y")
            time_process = datetime.strptime(time, "%H:%M:%S")
            new_time = datetime.strftime(time_process, "%H:%M")

        except ValueError:
            new_date = datetime.strftime(date, "%d-%m-%y")
            time_process = datetime.strptime(time, "%H:%M")
            new_time = datetime.strftime(time_process, "%H:%M")

    return new_date, new_time

def format_value(value_raw):
    #Solve the decimal point issue
    try:
        float_value = float(value_raw)
        if (float_value % 1 == 0):
            value = int(float_value)

        else:
            value = float_value

    #If the value cannot be converted to float
    except ValueError:
        value = value_raw

    finally:
        return value

if __name__ == "__main__":
    arr = os.listdir('./Source')

    for i in range(len(arr)):
        print(f"Detected file {arr[i]}, processing...")
        file_process(arr[i])
        print(f"File processed. New filename: Processed_{arr[i]}\n")

    print("All files processed.")