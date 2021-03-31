#!/usr/bin/env python3

from collections import Counter
from pathlib import Path
import csv
import datetime
import sys


def read_csv(csv_path):
    """ Converts csv file to list of orders (dicts) """

    def process(row):
        """ Helper function to parse row values correctly """
        def parse_date(date_str):
            m, d, y = [int(x) for x in date_str.split('/')]
            y += 2000
            return datetime.date(y, m, d)

        row['Order Date'] = parse_date(row.get('Order Date'))
        row['Item Total'] = float(row.get('Item Total').replace('$', ''))
        return row

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [process(row) for row in reader]


def get_stats(orders):
    """ extracts summary stats from order dict """

    totals = [order['Item Total'] for order in orders]
    dates = [dt.get('Order Date') for dt in orders]
    cats = [order.get('Category') for order in orders]

    return {
        'total': round(sum(totals), 2),
        'top_day': Counter([d.strftime("%A") for d in dates]).most_common(),
        'top_cats': [x[0] for x in Counter(cats).most_common() if x[0]][:3],
        'years': round((max(dates) - min(dates)).days / 365),
    }


def print_summary_stats(stats):
    summary_str = f"""In {stats['years']} years, I spent ${stats['total']:,}\n
                  I bought {', '.join(stats['top_cats'][1:])}.\n
                  And a lot of {stats['top_cats'][0]}."""

    print(summary_str)


def main():
    if len(sys.argv) < 2:
        print("CSV file required")
    else:
        filepath = Path(sys.argv[1])
        orders = read_csv(filepath)
        stats = get_stats(orders)
        print_summary_stats(stats)


if __name__ == "__main__":
    main()
