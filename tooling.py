# import matplotlib.pyplot as plt
import numpy as np


def find_day_of_year(year, month, day):
    """
    tool for finding the number of days in the month of a given year
    """

    days_per_month = np.array([
        31, #january
        28, #Feb
        31, #Mar
        30, #Apr
        31, #May
        30, #June
        31, #July
        31, #Aug
        30, #Sep
        31, #Oct
        30, #Nov
        31, #Dec
    ])
    # leap year case
    if year % 4 == 0:
        days_per_month[1] += 1
        
    day_of_year = np.sum(np.array(
        days_per_month[:month - 1])) + day - 1
    return day_of_year
    
    
    
def scatter(x,y):
   """
#    make a scatter plot with jitter
#    """
    x_jitter = x + np.random.normal(size=x.size, scale=.5)
   y_jitter = y + np.random.normal(size=y.size, scale=.5)

scatter(temps[:-1], temps[1:])



shift = 1

print(np.corrcoef(temps[:-shift], temps[shift:]))
