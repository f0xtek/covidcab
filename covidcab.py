#!/usr/bin/env python
from argparse import ArgumentParser
import csv
from collections import defaultdict, namedtuple
from datetime import datetime
import os

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

Journey = namedtuple('Journey', 'pickup dropoff passengers distance fare')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-f', "--file",
                        dest="filename",
                        default=f"{os.getcwd()}/yellow_tripdata_2020-04.csv",
                        help="The path to the CSV file containing journay data.")
    return parser.parse_args()


def parse_csv(filename):
    cab_journeys = defaultdict(list)
    with open(filename, encoding='utf-8') as f:
        for line in csv.DictReader(f):
            try:
                vendor_id = line['VendorID']
                pickup_datetime = datetime.strptime(line['tpep_pickup_datetime'], DATETIME_FORMAT)
                dropoff_datetime = datetime.strptime(line['tpep_dropoff_datetime'], DATETIME_FORMAT)
                passenger_count = int(line['passenger_count'])
                trip_distance = float(line['trip_distance'])
                total_fare = float(line['total_amount'])
            except ValueError:
                continue

            j = Journey(pickup=pickup_datetime, dropoff=dropoff_datetime, passengers=passenger_count,
                        distance=trip_distance, fare=total_fare)
            cab_journeys[vendor_id].append(j)
    return cab_journeys


def main():
    args = parse_args()
    cab_journeys = parse_csv(args.filename)
    print(cab_journeys)


if __name__ == '__main__':
    main()
