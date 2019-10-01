# import matplotlib.pyplot as plt
import numpy as np

import tools 

def get_data():

    weather_filename = 'weather_predictor/fort_lauderdale.csv'
    weather_file = open(weather_filename)
    weather_data = weather_file.read()
    weather_file.close()


    lines = weather_data.split('\n')
    labels = lines[0]
    values = lines[1:]
    n_values = len(values)



    year = []
    month = []
    day = []
    max_temp = []
    j_year = 1
    j_month = 2
    j_day = 3
    j_max_temp = 5


    for i_row in range(n_values):
        split_values = values[i_row].split(',')
        if len(split_values) >= j_max_temp:
            year.append(int(split_values[j_year]))
            month.append(int(split_values[j_month]))
            day.append(int(split_values[j_day]))
            max_temp.append(float(split_values[j_max_temp]))

# Examining the days list, and it matches with what we'd expect from before 
#for i_day in range(100): 
#    print(max_temp[i_day])
    
#plt.plot(max_temp)    
#plt.show()

    i_mid = len(max_temp) // 2
    temps = np.array(max_temp[i_mid:])
# year
    year = year[i_mid:]
# month
    month =month[i_mid:]
# day
    day = day[i_mid:]


    temps[np.where(temps == -99.9)] = np.nan

#plt.plot(temps, color='black', marker='.', linestyle='none')
#plt.show()



    i_start = np.where(np.logical_not(np.isnan(temps)))[0][0]
    temps = temps[i_start:]
    year = year[i_start:]
    month = month[i_start:]
    day = day[i_start:]


    i_nans = (np.where(np.isnan(temps))[0])

 
    for i in range(temps.size):
        if np.isnan(temps[i]):
            temps[i] = temps[i - 1]
    return (temps, year, month, day)



def find_autocorr():

    autocorr = []
    for shift in range(1,1000):
        correlation = (np.corrcoef(temps[:-shift], temps[shift:])[1,0])
        autocorr.append(correlation)



def build_temp_calendar(temps, year, month, day):
    
    day_of_year = np.zeros(temps.size) 
    for i_row in range(temps.size): 
        day_of_year[i_row] = tools.find_day_of_year(
            year[i_row], month[i_row], day[i_row])


    median_temp_calendar = np.zeros(366)
    ten_day_medians = np.zeros(temps.size)
    for i_day in range(0, 365):
    # create 10-day window
        low_day = i_day - 5
        high_day = i_day + 4
    
        if low_day < 0:
            low_day += 365
        if high_day > 365:
            high_day += -365
        if low_day < high_day: 
            i_window_days = np.where(
            np.logical_and(day_of_year >= low_day,
            day_of_year <= high_day))
        else: 
            i_window_days = np.where(
            np.logical_or(day_of_year >=low_day,
                day_of_year <= high_day))

        ten_day_median = np.median(temps[i_window_days])
        median_temp_calendar[i_day] = ten_day_median
        ten_day_medians[np.where(day_of_year == i_day)] = ten_day_median
    #Handle '364' years, to be handled the same as normal years, to make things easier
        if i_day ==364: 
            ten_day_medians[np.where(day_of_year == 365)] = ten_day_median
            median_temp_calendar[365] = ten_day_median

    return median_temp_calendar

 

def predict (year, month, day, temperature_calendar):
   
    day = tools.find_day_of_year(year, month, day)
    prediction = temperature_calendar[day]
    return prediction 
    

if __name__ == '__main__': 
    temps, year, month, day = get_data()
    temp_calendar = build_temp_calendar(temps, year, month, day)
    for test_day in range(1,30): 
        test_year = 2016
        test_month = 6
        prediction = predict(test_year, test_month, test_day, temp_calendar)
        print(test_year, test_month, test_day, prediction)