import time
import pandas as pd
import numpy as np
import calendar 

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month = ['january', 'february', 'march', 'april', 'may', 'june']
week_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


line_lenght = 90

# print long string with repeating char, used to separate sections of output
print_line = lambda char: print(char[0] * line_lenght)

def print_processing_time(initial_time):
    time_str = "[... %s seconds]" % round((time.time() - initial_time), 3)
    print(time_str.rjust(line_lenght))
    print_line('-')

def get_filter_city():
    """
    Asks user to specify a city.

    Returns:
        (str) city - name of the city to analyze
    """
    # build and display the list of cities for which we have datasets
    cities_list = []
    cities_number = 0

    for a_city in city_data:
        cities_list.append(a_city)
        cities_number += 1
        print('        {0:20}. {1}'.format(cities_number, a_city.title()))

    # ask user to input a number for a city from the list; easier for user than string input
    while True:
        try:
            city_number = int(input("\n    Enter a number for the city (1 - {}):  ".format(len(cities_list))))
        except:
            continue

        if city_number in range(1, len(cities_list)+1):
            break

    # get the city's name in string format from the list
    city = cities_list[city_number - 1]
    return city

def get_filter_month():
    """
    Asks user to specify a month to filter on, or choose all.

    Returns:
        (str) month - name of the month to filter by, or "all" for no filter
    """
    while True:
        try:
            month = input("    Enter the month with January=1, June=6 or 'a' for all:  ")
        except:
            print("        ---->>  Valid input:  1 - 6, a")
            continue

        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = month[int(month) - 1]
            break
        else:
            continue
    
    return month

def get_filter_day():
    """
    Asks user to specify a day to filter on, or choose all.

    Returns:
        (str) day - day of the week to filter by, or "all" for no filter
    """
    while True:
        try:
            day = input("    Enter the day with Monday=1, Sunday=7 or 'a' for all:  ")
        except:
            print("        ---->>  Valid input:  1 - 7, a")
            continue

        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            # reassign the string name for the day
            day = week_day[int(day) - 1]    # here we MUST -1 to get correct index
            break
        else:
            continue

    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print_line('=')
    print('\n  Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington).
    #  HINT: Use a while loop to handle invalid inputs

    city = get_filter_city()

    # get user input for month (all, january, february, ... , june)
    month = get_filter_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_filter_day()

    return city, month, day

def filter_summary(city, month, day, init_total_rides, data_frame1):
    """
    Displays selected city, filters chosen, and simple stats on dataset.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int) init_total_rides - total number of rides in selected city before filter
        (dataframe) data_frame1 - filtered dataset
    """
    initial_time = time.time()

    filtered_rides = len(data_frame1)
    num_stations_start = len(data_frame1['Start Station'].unique())
    num_stations_end = len(data_frame1['End Station'].unique())

    print('  Gathering statistics for:      ', city)
    print('    Filters (month, day):        ', month, ', ', day)
    print('    Total rides in dataset:      ', init_total_rides)
    print('    Rides in filtered set:       ', filtered_rides)
    print('    Number of start stations:    ', num_stations_start)
    print('    Number of end stations:      ', num_stations_end)

    print_processing_time(initial_time)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data_frame1 - Pandas DataFrame containing city data filtered by month and day
    """
    initial_time = time.time()

    # load data file into a dataframe
    data_frame1 = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    data_frame1['Start Time'] = pd.to_datetime(data_frame1['Start Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    data_frame1['month'] = data_frame1['Start Time'].dt.month                 # range (1-12)
    data_frame1['day_of_week'] = data_frame1['Start Time'].dt.dayofweek       # range (0-6)
    data_frame1['hour'] = data_frame1['Start Time'].dt.hour                   # range (0-23)

    init_total_rides = len(data_frame1)
    filtered_rides = init_total_rides    # initially

    # filter by month if applicable
    if month != 'all':
        # use the index of the month list to get the corresponding int
        month_i = month.index(month) + 1     # index() returns 0-based, so +1
    
        # filter by month to create the new dataframe
        data_frame1 = data_frame1[data_frame1.month == month_i]
        month = month.title()

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the week_day list to get the corresponding int
        day_i = week_day.index(day)         # index() returns 0-based, matches data_frame1

        # filter by day of week to create the new dataframe
        data_frame1 = data_frame1[data_frame1.day_of_week == day_i]
        day = day.title()

    print_processing_time(initial_time)

    filter_summary(city.title(), month, day, init_total_rides, data_frame1 )

    return data_frame1

def hour_12(hour):
    """
    Converts an int hour time to string format with PM or AM.

    Args:
        (int) hour - int representing an hour
    Returns:
        (str) str_hour - string with time in 12 hour format
    """

    if hour == 0:
        str_hour = '12 AM'
    elif hour == 12:
        str_hour = '12 PM'
    else:
        str_hour = '{} AM'.format(hour) if hour < 12 else '{} PM'.format(hour - 12)

    return str_hour

def time_stats(data_frame1):
    """Displays statistics on the most frequent times of travel."""

    print('  Most Frequent Times of Travel...')
    initial_time = time.time()

    # display the most common month; convert to string
    month = month[data_frame1['month'].mode()[0] - 1].title()
    print('    Month:               ', month)

    # display the most common day of week
    common_day = data_frame1['day_of_week'].mode()[0]        # day in data_frame1 is 0-based
    common_day = week_day[common_day].title()
    print('    Day of the week:     ', common_day)

    # display the most common start hour; convert to 12-hour string
    hour = hour_12(data_frame1['hour'].mode()[0])
    print('    Start hour:          ', hour)

    print_processing_time(initial_time)

def station_stats(data_frame1):
    """Displays statistics on the most popular stations and trip."""

    print('  Most Popular Stations and Trip...')
    initial_time = time.time()

    filtered_rides = len(data_frame1)

    # display most commonly used start station
    start_station = data_frame1['Start Station'].mode()[0]
    start_station_trips = data_frame1['Start Station'].value_counts()[start_station]

    print('    Start station:       ', start_station)
    print('{0:30}{1}/{2} trips'.format(' ', start_station_trips, filtered_rides))

    # display most commonly used end station
    end_station = data_frame1['End Station'].mode()[0]
    end_station_trips = data_frame1['End Station'].value_counts()[end_station]

    print('    End station:         ', end_station)
    print('{0:30}{1}/{2} trips'.format(' ', end_station_trips, filtered_rides))

    # display most frequent combination of start station and end station trip
    # group the results by start station and end station
    data_frame1_start_end_combination_gd = data_frame1.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = data_frame1_start_end_combination_gd['Trip Duration'].count().max()
    most_freq_trip = data_frame1_start_end_combination_gd['Trip Duration'].count().idxmax()

    print('    Frequent trip:        {}, {}'.format(most_freq_trip[0], most_freq_trip[1]))
    print('{0:30}{1} trips'.format(' ', most_freq_trip_count))

    print_processing_time(initial_time)

def seconds_to_HMS_str(total_seconds):
    """
    Converts number of seconds to human readable string format.

    Args:
        (int) total_seconds - number of seconds to convert
    Returns:
        (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
    """

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    
    day_hour_str = ''
    if weeks > 0:
        day_hour_str += '{} weeks, '.format(weeks)
    if days > 0:
        day_hour_str += '{} days, '.format(days)
    if hours > 0:
        day_hour_str += '{} hours, '.format(hours)
    if minutes > 0:
        day_hour_str += '{} minutes, '.format(minutes)

    # always show the seconds, even 0 secs when total > 1 minute
    if total_seconds > 59:
        day_hour_str += '{} seconds'.format(seconds)

    return day_hour_str

def trip_duration_stats(data_frame1):
    """Displays statistics on the total and average trip duration."""

    print('  Trip Duration...')
    initial_time = time.time()

    # display total travel time; cast to int, we don't need fractions of seconds!
    total_travel_time = int(data_frame1['Trip Duration'].sum())
    print('    Total travel time:   ', total_travel_time, 'seconds')
    print('                             ', seconds_to_HMS_str(total_travel_time))

    # display mean travel time
    mean_travel_time = int(data_frame1['Trip Duration'].mean())
    print('    Mean travel time:    ', mean_travel_time, 'seconds')
    print('                             ', seconds_to_HMS_str(mean_travel_time))

    print_processing_time(initial_time)

def user_stats(data_frame1):
    """Displays statistics on bikeshare users."""

    print('  User Stats...')
    initial_time = time.time()

    # Display counts of user types
    user_types = data_frame1['User Type'].value_counts()
    for idx in range(len(user_types)):
        val = user_types[idx]
        user_type = user_types.index[idx]
        print('    {0:21}'.format((user_type + ':')), val)

    # 'Gender' and 'Birth Year' is only available for Chicago and New York City
    # Check for these columns before attempting to access them

    if 'Gender' in data_frame1.columns:
        # Display counts of gender
        genders = data_frame1['Gender'].value_counts()
        for idx in range(len(genders)):
            val = genders[idx]
            gender = genders.index[idx]
            print('    {0:21}'.format((gender + ':')), val)

    if 'Birth Year' in data_frame1.columns:
        # Display earliest, most recent, and most common year of birth
        print('    Year of Birth...')
        print('        Earliest:        ', int(data_frame1['Birth Year'].min()))
        print('        Most recent:     ', int(data_frame1['Birth Year'].max()))
        print('        Most common:     ', int(data_frame1['Birth Year'].mode()))

    print_processing_time(initial_time)

def display_raw_data(data_frame1):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1    # use index values for rows

    print('\n    Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (y or n):  ')
        if raw_data.lower() == 'y':
            # display show_rows number of lines, but display to user as starting from row as 1
            # e.g. if rows_start = 0 and rows_end = 4, display to user as "rows 1 to 5"
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', data_frame1.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print_line('.')
            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        data_frame1 = load_data(city, month, day)

        time_stats(data_frame1)
        station_stats(data_frame1)
        trip_duration_stats(data_frame1)
        user_stats(data_frame1)
        display_raw_data(data_frame1)

        restart = input('\n    Would you like to restart? (y or n):  ')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
