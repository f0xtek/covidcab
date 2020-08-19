#!/usr/bin/env python
from argparse import ArgumentParser
import csv
from collections import defaultdict, namedtuple
from datetime import datetime
import os
import statistics
from tabulate import tabulate

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
PRINT_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

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
                pickup_datetime = datetime.strptime(line['tpep_pickup_datetime'],
                                                    DATETIME_FORMAT).strftime(PRINT_DATETIME_FORMAT)
                dropoff_datetime = datetime.strptime(line['tpep_dropoff_datetime'],
                                                     DATETIME_FORMAT).strftime(PRINT_DATETIME_FORMAT)
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
                    statistics.mean([journey.passengers for journey in journeys if type(journey) == Journey]), 1)
        )
        cab_journeys[vendor].append(va)
    return cab_journeys


def vendor_totals(cab_journeys):
    for vendor, journeys in cab_journeys.items():
        vt = VendorTotals(distance=round(
                    sum([journey.distance for journey in journeys if type(journey) == Journey]), 2))
        cab_journeys[vendor].append(vt)
    return cab_journeys


def print_results(total_distance, total_fare, total_passengers, cab_journeys):
    print(f'In New York during the first week of April 2020, amidst a state-wide lockdown, {total_passengers} people '
          f'travelled a total of {total_distance} miles by Yellow Cab.')
    print('A total of ${:.2f} was spent on cab journeys during this time period.'.format(total_fare), end="\n\n")
    print('Below is a breakdown of the top 50 journeys sorted by distance travelled for each Yellow Cab vendor:',
          end="\n\n")
    for vendor, journeys in cab_journeys.items():
        print(f'Vendor ID: {vendor}', end="\n\n")
        data = journeys[:-2]
        headers = ["Pickup", "Dropoff", "Passengers", "Distance", "Fare"]
        print(tabulate(data, headers=headers, floatfmt=".2f"))
        for journey in cab_journeys[vendor]:
            if type(journey) == VendorTotals:
                print()
                data = [journey]
                headers = ["Total Distance (miles)"]
                print(tabulate(data, headers=headers, floatfmt=".2f"))
            elif type(journey) == VendorAverages:
                print()
                data = [journey]
                headers = ["Average Distance (miles)", "Average Fare ($)", "Average Passengers"]
                print(tabulate(data, headers=headers, floatfmt=".2f"))
        print()


def main():
    args = parse_args()
    cab_journeys = parse_csv(args.filename)
    ttl_distance = total_distance(cab_journeys)
    ttl_fares = total_fare(cab_journeys)
    ttl_passengers = total_passengers(cab_journeys)
    cab_journeys = vendor_averages(cab_journeys)
    cab_journeys = vendor_totals(cab_journeys)
    print_results(ttl_distance, ttl_fares, ttl_passengers, cab_journeys)


if __name__ == '__main__':
    main()
