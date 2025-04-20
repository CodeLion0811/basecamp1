from collections import defaultdict
import pandas as pd
import numpy as np

# Loading the CSV file
df = pd.read_csv('city_temperature.csv', parse_dates=['Date'], dayfirst=True)
# print(df)


# New table with Date, City, Temperature columns
df = df.melt(id_vars=['Date'], var_name='City', value_name='Temperature')

df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
df.dropna(subset=['Temperature'], inplace=True)

# Grouping data by city
cities = df['City'].unique()
# print(cities)

# Max temperature  
def get_max_temp_day(df):
    result = {}
    for city in cities:
        city_df = df[df['City'] == city]
        max_row = city_df.loc[city_df['Temperature'].idxmax()]
        result[city] = (max_row['Date'], max_row['Temperature'])
    return result

# Monthly average temperature 
def get_monthly_avg_temp(df):
    df['Month'] = df['Date'].dt.month
    monthly_avg = df.groupby(['City', 'Month'])['Temperature'].mean().reset_index()
    result = defaultdict(dict)
    for _, row in monthly_avg.iterrows():
        result[row['City']][int(row['Month'])] = row['Temperature']
    return result


# 3️⃣ Count 5-day  above monthly average
def count_sliding_windows_above_avg(df):
    df['Month'] = df['Date'].dt.month
    monthly_avg = get_monthly_avg_temp(df)
    result = {}

    for city in df['City'].unique():
        city_df = df[df['City'] == city].sort_values('Date')
        temps = city_df['Temperature'].values
        months = city_df['Month'].values

        count = 0
        for i in range(len(temps) - 4):
            window_temp = temps[i:i+5]
            window_month = months[i:i+5]
            if len(set(window_month)) == 1:  # same month
                avg_temp = monthly_avg[city][window_month[0]]
                if np.all(window_temp > avg_temp):
                    count += 1
        result[city] = count
    return result

# functions
max_temp_days = get_max_temp_day(df)
# Print results
print("\nMax Temperature Day per City:\n")
for city, (date, temp) in max_temp_days.items():
    print(f"{city}: {temp}°C on {date}")


print("\n------------------------------------------\n")

monthly_avg = get_monthly_avg_temp(df)
print("Monthly Average Temperatures:\n")
for city, months in monthly_avg.items():
    print(f"{city}: " + ", ".join([f"{month}: {round(temp, 2)}°C" for month, temp in months.items()]))

print("\n------------------------------------------\n")


sliding_window_counts = count_sliding_windows_above_avg(df)
print("Sliding Windows Above Monthly Average:\n")
for city, count in sliding_window_counts.items():
    print(f"{city}: {count} window(s)")



