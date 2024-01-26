#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Eva Balogun, Sacha Sergent, Sydney Schulz
12/1/2022
DS 2001 project

Problem statemenet and background: 
CHAARG is a national organization with 10 000 members who pay dues which pay 
the salaries of its team. Retention is a crucial way to maintain memberships
and therefore dues to keep the organization running. At Northeastern, there are
200-300 members each semester. How can NU CHAARG optimize retention efforts?
Is there a correlation between event attendance and renewal rates? Are there
specific events that seem to foster higher renewal than others?
    
Introduction and description of the data:
The data is attendance and participation data recorded manually throughout the 
spring semester of 2022 by NU CHAARG's secretary. Each column is an event while
each row is a club member (the first few columns are for member information 
such as email). If a club member attended a workout, they got 2 points. 
If they attended a social, they earned 3 points. For small group events, they 
earned 1 point, etc. These points helped track attendance and club engagement. 

Methods:
This code start out by reading the data into a list of lists. 
In the split function, the data is split into equal bins in order to then 
generate two histograms: one showing members organized by percentiles of
activity rate versus renewal rate, another showing the same thing with
activity rate solely considering weekly workouts. 
Attendance data for events is also organized so that the events can be plotted
according to how many people attended them, and of those how many renewed

Results, Conclusions and Future Work:
The bar graph that includes member's engagement via attendance at all events is 
more steadily increasing and linear than the graph that only includes workouts. 
This suggests that overall club engagement may be a better indicator of
whether a member will renew or not than only weekly workout engagement. Club 
leaders could maybe focus on promoting socials and other events during the year.
The histogram containing only data about weekly workouts provides the insight
that no members who went to no weekly workouts renewed, suggesting that club
leaders should focus on making sure every member attends at least one workout
in order to increase retention. One limitation of our study is that it doesn’t 
account for external factors. Some members might have not renewed for reasons 
outside of engagement or how much they enjoyed CHAARG (i.e. co-op, a busy 
schedule, dues). Workout attendance might have also been affected by external 
factors such as weather or how far the event is from campus. Future work may
account for some of these factors such as analyzing subsets of the data 
including only non-graduating members, only members who were not going on coop,
etc.
"""

DATA = "CHAARG_S22.csv"
SHORTDATA = "CHAARG_S22_short.csv"

import matplotlib.pyplot as plt

def read_data_names(filename):
    """
    Reads in data from a list of lists to 2 smaller, filtered list of lists

    Parameters
    ----------
    filename : list of lists
        the data being read in.

    Returns
    -------
    full_data : list of lists
        the data being read in with only the columns containing ints.
    ww_data : list of lists
        the data being read in with only the desired weekly workout columns.
    """
    file = open(filename, "r")

    #skip the headers

    headers = []
    headers = file.readline()
    headers = headers.strip().split(",")
    headers.append(headers)
    
    

    # isolate the weekly workout columns
    
    ww_columns = []
    
    for item in headers:
        if item[:2] == "WW":
            ww_columns.append(item)
    
    # create lists to read the data into
    
    ww_data = []
    full_data = []
    
    # iterate through the file
    
    for line in file:
        pieces = line.strip().split(",")
        
        
        # start the inner lists with each member's last name only
        row = [pieces[1]]
        rows = [pieces[1]]
        
        # account for people counted twice in the renewal column
        for i in range(len(pieces)):
            if int(pieces[-1]) < 2:
                pieces[-1] = pieces[-1]
            else:
                pieces[-1] = 1
        
        # skip rows that do not belong to a member
        # (like the final row, which is the totals of each column)
        if pieces[1] != "":
            ww_data.append(row)
            full_data.append(rows)
        
        # for the weekly workout list, only use weekly workout data
        for i in range(len(pieces)):
            if headers[i] in ww_columns:
                if pieces[i] == "":
                    pieces[i] = 0
                else:
                    pieces[i] = int(pieces[i])
                row.append(pieces[i])
                
            # replace all strings with zeroes
            if headers[i] != "FIRST NAME" and headers[i] != "LAST NAME" and headers[i] != "E-MAIL" and headers[i] != "SGC":

                if pieces[i] != "excused" and pieces[i] != "unexcused" and pieces[i] != "" :
                    pieces[i] = int(pieces[i])
                else:
                    pieces[i] = 0
                rows.append(pieces[i])
    
    renewal = []
    for i in range(len(full_data)):
        renewal.append(full_data[i][-1])
        

    file.close()
    return ww_data, full_data, renewal, headers


def data_sort(data, renewal, full=True):
    """
    sorts the data into 2 new lists, each made up of floats where the number
    prior to the period signifies a number of points and the number after the
    period signifies whether that person renewed (1 if they renewed, else 0)

    Parameters
    ----------

    data : list of lists
        each member's attendance record through the semester for events.
    renewal : list
        list of zeroes and ones representing whether or not someone renewed
    full : optional parameter, bool
        if True, data includes "Renewal?" column
    
    Returns
    -------
    floats_list: list
        list of floats where the number before the decimal is the person's 
        points and the number following the decimal is whetehr they renewed.

    """
    # start a list where each index will be a person's total points
    attendance = []
    
    # iterate through each person's data
    for line in data:
        # create a list of only each person's points
        total_points = []
        
        # skip the last value if the data includes the "Renewal?" column
        if full==True:
            total_points.append(line[1:-1])
        else: 
            total_points.append(line[1:])
        
        # total the person's points, divide by two for the attendance number
        # add that total points to the attendance list
        chaargie_points = int(sum(total_points[0])/2)
        points_individual = (str(chaargie_points))
        
        attendance.append(points_individual)
    
    # create a list where the now known attendance points can be associated
    # to whether or not that same member renewed
    floats_list =[]

    for i in range(len(attendance)):
        # create a decimal where points are on the left, if renewed on right
        new_num = str(attendance[i]) + (".") + str(renewal[i])
        new_num = float(new_num)
        floats_list.append(new_num)
    
    # sort the list of floats so they can be manipulated for visualization
    floats_list.sort()
    
    
    return floats_list


def split(data):
    """
    splits data from a list of floats into ten lists of lists of equal size

    Parameters
    ----------
    data : list
        list of floats.

    Returns
    -------
    bins_lists : list of lists
        each inner-list is of equal magnitude.

    """
    size_data = len(data)
    
    # figure out how many items will go in each inner list 
    # make sure it is an even integer of items per list
    
    size_data = len(data)
    remainder = size_data % 10
    if remainder != 0:
        subtract = size_data - remainder
        data = data[:subtract]
    
    
    # creating the amount of participants to go into each percentile
    size = int((size_data - size_data%10)/10)
         
    # create the list of lists
    bins_lists = []
    
    # iterate through the whole data 
    while len(data) > size:
         # create an inner list with the first values from the data
         pice = data[:size]
         bins_lists.append(pice)
         # update the data to remove values that have now been added as a list
         data = data[size:]
    
    bins_lists.append(data)
     
    return bins_lists
    
def seperate_and_plot(data, title, color):
    """
    separate a list of lists into bins and plot on a histogram

    Parameters
    ----------
    data : list of lists
        list of lists of equal magnitude
    title : string
        name of the histogram.
    color : string
        color of the histogram.

    Returns
    -------
    None.

    """
    
    main_list = []
    
   # splitting the data points by the decimal point and adding that info
   # to a seperate list so each list within a list within a list contains 
   # the total points and renewal for each participants
    for bin_list in data:
       bins = []
       for point in bin_list:
           point = str(point)
           split = point.strip().split(".")
           bins.append(split)
       main_list.append(bins)
       
   # creating empty dict that will contain the perctile as key
   # and how many renewed as value    
    dictionary = {}
   
    count = 0

    for outer_list in main_list:
       total_points = 0
       for inner_list in outer_list:
           # adding the points for each point in the list of lists of lists
           point = float(inner_list[1])
           total_points += point
           
       dictionary[count] = total_points
       # increasing count by 10 so the percentile goes up by 10
       count += 10
   
    # defining percentiles and points
    percentiles = list(dictionary.keys())
    points = list(dictionary.values())
   
    # plotting bar graph
    plt.figure(figsize = (10, 5))
    plt.bar(percentiles, points, color = color, width = 7)
    plt.xlabel("Percentile of events attended")
    plt.ylabel("No. of students who renewed")
    plt.title(title)
    plt.show()

def data_events(data, headers, whole_data = True):
    """
    Creates a list of total attendance for each weekly workout (sums columns)
    and a list of names of weekly workouts

    Parameters
    ----------
    data : list of lists
        each inner list represents a member's attendance through the semester.
    headers : list
        list of strings, the headers of every column in the data.
    whole_data : bool, optional
        whether the whole dataset is being used or only a subset such as only
        weekly workout columns. The default is True.

    Returns
    -------
    attendance : list
        list of numbers of people who attended an event.
    ww_columns : list
        list of strings containg the names of weekly workouts.

    """
    # exclude columns that are not included in the data used for this function 
    headers = headers[4:]
    
    # create a list of weekly workout names and a list of their indexes
    ww_columns = []
    ww_col_num = []
    for item in headers:
        if item[:2] == "WW":
            ww_columns.append(item)
            ww_col_num.append(headers.index(item))
    
    # exclude the "Renewal?" column if it is included in the data 
    if whole_data == True:
        # remove the first column (person's name) from the data
        for i in range(len(data)):
            data[i] = data[i][1:]
    
    # create an attendance list
    attendance = []
    
    # iterate through the weekly workouts
    for item in ww_col_num:
        col_num = item
        # start an attendnace counter for each event
        event = 0
        # update the attendnace counter by iterating through each row
        for i in range (len(data)):
            event += data[i][col_num]
        
        # divide by two to count attendance rather than points
        attendance.append(int(event/2)) 
    
    return attendance, ww_columns
       
def renewed_only(data):
    """
    generates a list of the data for only renewed members

    Parameters
    ----------
    data : list of lists
        data for all members where each row is a member 
        and each column an event.

    Returns
    -------
    updated_data : list of lists
        same list as data with only renewed members.

    """
    updated_data = []
    
    # iterate through each row, only append the new list with those for whom
    # "Renewal?" is equal to 1
    for i in range (len(data)):
        if data[i][-1] == 1:
            updated_data.append(data[i])
    
    return updated_data 

def attendance_percent(attendance_renewed, attendance_full):
    """
    Converts numbers in one list to what percent of the number in another list 
    at the same position is

    Parameters
    ----------
    attendance_renewed : list
        list of ints.
    attendance_full : list
        list of ints.

    Returns
    -------
    attendance_renewed : list
        list of floats.

    """
    # iterate through the list to be modified
    for i in range(len(attendance_renewed)):
        # convert each number to a percent of the corresponding number in 
        # another list
        attendance_renewed[i] = attendance_renewed[i]*100/attendance_full[i]
    
    return attendance_renewed
    
def graph_attendance(attendance_full, attendance_renewed, ww_columns):
    """
    Generates a scatter plot of events based on how many peopel attended in 
    total and of those, how many renewed

    Parameters
    ----------
    attendance_full : list
        list of ints, total attendance for each event.
    attendance_renewed : list
        list of ints, attendance only if a person renewed for each event.
    ww_columns : list
        list of strings where each str is the name of an event

    Returns
    -------
    None.

    """
    plt.figure(figsize=(6,6), dpi=200)
    plt.grid()
    
    # iterate through the names of weekly workouts and plot them according
    # to their total attendance and 
    for i in range(len(ww_columns)):
        plt.scatter(attendance_full[i], attendance_renewed[i], 
                    label = ww_columns[i])
    plt.xlabel("Total number of people who attended the event")
    plt.ylabel("Percent of people who attended and renewed")
    plt.title("Each event according to how many people attended, and of those what % many renewed")
    x_line = [0,100]
    y_line = [50,50]
    plt.plot(x_line, y_line, color = "gold")
    plt.show()
    
def main():

    # Read in the data
    ww_data, full_data, renewal, headers = read_data_names(DATA)
    
    # Create lists with the data to be plotted into histograms
    floats_list_ww = data_sort(ww_data, renewal, full=False) 
    floats_list_total = data_sort(full_data, renewal, full=True)
    
    # Modify the lists to be plotted into histograms so that they are in bins
    bins_lists_ww = split(floats_list_ww)
    bins_lists_total = split(floats_list_total)

    # Plot the bins on histograms
    seperate_and_plot(bins_lists_ww, 
                      "Attendance vs Renewal For Only Weekly Workouts", 
                      color = "turquoise")
    
    seperate_and_plot(bins_lists_total, "Attendance vs Renewal For All Events", 
                      color = "lightpink")
    
    # Extract attendance from the data
    attendance_full, ww_columns = data_events(full_data, headers)
    
    # Filter the data so it only contains members who renewed
    renewed = renewed_only(full_data)
    
    # Extract attendance for only those who renewed from the data
    attendance_renewed, ww_columns = data_events(renewed, headers, 
                                                 whole_data=False)
    
    # Modify attendance for only those who went to an event and renewed
    # to a percentage 
    attendance_renewed = attendance_percent(attendance_renewed,attendance_full)
    
    # Graph the attendance at events versus what % of those who went renewed
    graph_attendance(attendance_full, attendance_renewed, ww_columns)
    
if __name__ == "__main__": 
    main()