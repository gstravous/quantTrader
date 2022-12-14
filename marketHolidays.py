import numpy as np
import datetime as dt

market_holidays = [np.datetime64('2022-01-17'),
                   np.datetime64('2022-02-21'),
                   np.datetime64('2022-04-15'),
                   np.datetime64('2022-05-30'),
                   np.datetime64('2022-06-20'),
                   np.datetime64('2022-07-04'),
                   np.datetime64('2022-09-05'),
                   np.datetime64('2022-11-24'),
                   np.datetime64('2022-12-26'),
                   np.datetime64('2023-01-02'),
                   np.datetime64('2023-01-16'),
                   np.datetime64('2023-02-20'),
                   np.datetime64('2023-04-07'),
                   np.datetime64('2023-05-29'),
                   np.datetime64('2023-06-19'),
                   np.datetime64('2023-07-04'),
                   np.datetime64('2023-09-04'),
                   np.datetime64('2023-11-23'),
                   np.datetime64('2023-12-25'),
                   np.datetime64('2024-01-15'),
                   np.datetime64('2024-02-19'),
                   np.datetime64('2024-05-27'),
                   np.datetime64('2024-09-02'),
                   np.datetime64('2024-11-28'),
                   np.datetime64('2024-03-29')]


def add_market_days(start_date, market_days):
    days_elapsed = 0
    while days_elapsed < market_days:
        start_date = start_date + np.timedelta64(1, 'D')
        if not (start_date.astype(dt.datetime).weekday() > 4 or start_date in market_holidays):
            days_elapsed += 1

    return start_date
