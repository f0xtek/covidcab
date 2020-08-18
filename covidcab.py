#!/usr/bin/env python
from argparse import ArgumentParser
import csv
from collections import defaultdict, namedtuple
from datetime import datetime
import os
import statistics

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

Journey = namedtuple('Journey', 'pickup dropoff passengers distance fare')
VendorAverages = namedtuple('VendorAverages', 'distance fare passengers')
VendorTotals = namedtuple('VendorTotals', 'distance')


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
                distance = float(line['trip_distance'])
                fare = float(line['total_amount'])
            except ValueError:
                continue

            j = Journey(pickup=pickup_datetime, dropoff=dropoff_datetime, passengers=passenger_count,
                        distance=distance, fare=fare)
            cab_journeys[vendor_id].append(j)

    for key, value in cab_journeys.items():
        cab_journeys[key] = sorted(value, key=lambda x: x.distance, reverse=True)[:50]

    return cab_journeys


def total_distance(cab_journeys):
    distances_per_vendor = [
        [journey.distance for journey in journeys if type(journey) == Journey] for journeys in cab_journeys.values()]
    return round(sum([x for y in distances_per_vendor for x in y]), 1)


def total_fare(cab_journeys):
    fares_per_vendor = [
        [journey.fare for journey in journeys if type(journey) == Journey] for journeys in cab_journeys.values()]
    return round(sum([x for y in fares_per_vendor for x in y]), 2)


def total_passengers(cab_journeys):
    passengers_per_vendor = [
        [journey.passengers for journey in journeys if type(journey) == Journey] for journeys in cab_journeys.values()]
    return sum([passenger for passengers in passengers_per_vendor for passenger in passengers])


def avg_distance(cab_journeys):
    return statistics.mean([journey.distance for journey in cab_journeys.values()])


def vendor_averages(cab_journeys):
    for vendor, journeys in cab_journeys.items():
        va = VendorAverages(
            distance=round(
                    statistics.mean([journey.distance for journey in journeys if type(journey) == Journey]), 2),
            fare=round(
                    statistics.mean([journey.fare for journey in journeys if type(journey) == Journey]), 2),
            passengers=round(
                    statistics.mean([journey.passengers for journey in journeys if type(journey) == Journey]), 2)
        )
        cab_journeys[vendor].append(va)


def vendor_totals(cab_journeys):
    for vendor, journeys in cab_journeys.items():
        vt = VendorTotals(distance=round(
                    statistics.mean([journey.distance for journey in journeys if type(journey) == Journey]), 2))
        cab_journeys[vendor].append(vt)


def sort_vendor_by_total_distance(cab_journeys):
    pass


def print_results(cab_journeys):
    pass


def main():
    args = parse_args()
    cab_journeys = parse_csv(args.filename)
    ttl_distance = total_distance(cab_journeys)
    ttl_fares = total_fare(cab_journeys)
    ttl_passengers = total_passengers(cab_journeys)
    vendor_averages(cab_journeys)
    vendor_totals(cab_journeys)
    print(cab_journeys)


if __name__ == '__main__':
    main()
