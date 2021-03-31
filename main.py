#!/usr/bin/env python3

import sys
import pandas as pd

if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = "/Users/isaac/Desktop/01-Jan-2011_to_31-Mar-2021.csv"


def main():
    df = pd.read_csv(filepath)

    df['Item Total'] = df['Item Total'].str.replace('$', '', regex=False)

    total = sum(df['Item Total'].astype('float'))

    l_idx = len(df['Order Date']) - 1
    date_range = f"{df['Order Date'][0]} - {df['Order Date'][l_idx]}"

    print(f"You spent {total} during {date_range}")


if __name__ == "__main__":
    main()
