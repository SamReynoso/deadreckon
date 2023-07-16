import csv
import datetime
import pandas as pd

def inits():
    headings = ["lat/long", "date"]
    with open("files/coordinates.csv", "w") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",")
            csv_writer.writerow(headings)
    headings = [
            "windV", "windD",
            "waterV", "waterD",
            "craftV", "craftD",
            "date"
        ]
    with open("files/instruments.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow(headings)

def send_instruments(row: list):
    with open("files/instruments.csv", "a") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow(row)


def fetch_instruments() -> list:
    with open("files/instruments.csv", "r", encoding="utf-8", errors="ignore") as csvfile:
        final_line = csvfile.readlines()[-1]
        data = [ float(i) for i in list(csv.reader([final_line]))[0]]
        return data
     

def update_craft(craft_data):
    df = pd.read_csv("files/instruments.csv")
    df.loc[df.index[-1], "craftV"] = craft_data[0]
    df.loc[df.index[-1], "craftD"] = craft_data[1]
    df.to_csv("files/instruments.csv", index=False)


def send_coord(row: list):
    row.append(datetime.datetime.now())
    with open("files/coordinates.csv", "a") as csvfile:
        csv_write = csv.writer(csvfile, delimiter=",")
        csv_write.writerow(row)

def fetch_coordinates():
    with open("files/coordinates.csv", "r", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        reader.__next__()
        lat = []
        long = []
        for row in reader:
            lat.append(float(row[0]))
            long.append(float(row[1]))
        return lat, long