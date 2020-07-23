# date in yyyy/mm/dd format
import csv
import math
from datetime import timedelta, datetime

from Core.settings import CSVDownloadsPath

hourToSeconds = 3600
minutesToSeconds = 60


def read_event_times():
    with open(CSVDownloadsPath + 'event_times.csv') as csvDataFile:
        event_times = dict()
        csvReader = csv.reader(csvDataFile)
        print('file opened')
        next(csvReader)
        for row in csvReader:
            event = row[0]
            if (event in event_times.keys()) != True:
                event_times[event] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
        return event_times


# Comparing the dates will return
# either True or False
def updateEventTimers():
    event_times = read_event_times()
    timeUntilEvent = dict()
    for event in event_times:
        currentTime = datetime.now()
        eventTime = event_times[event]
        if eventTime < currentTime:
            addedTime = timedelta(days=5, hours=4)
            eventTime = eventTime + addedTime
            event_times[event] = eventTime
            print(event + ' is out of date, it was fixed')
            totalSeconds = eventTime - currentTime
            totalDays = totalSeconds.days
            totalSeconds = totalSeconds.total_seconds()

            remainingSeconds = (totalSeconds % hourToSeconds)
            hoursInSeconds = totalSeconds - remainingSeconds
            totalHours = hoursInSeconds / hourToSeconds
            totalHours = totalHours - (totalDays * 24)
            remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
            totalMinutes = (totalSeconds - hoursInSeconds) / 60
            totalMinutes = math.floor(totalMinutes)
            timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(
                totalMinutes) \
                        + ' minutes'
            timeUntilEvent[event] = timeUntil
            # print('Next occurance is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) + ' minutes')

        elif (currentTime < eventTime):
            totalSeconds = eventTime - currentTime
            totalDays = totalSeconds.days
            totalSeconds = totalSeconds.total_seconds()

            remainingSeconds = (totalSeconds % hourToSeconds)
            hoursInSeconds = totalSeconds - remainingSeconds
            totalHours = hoursInSeconds / hourToSeconds
            totalHours = totalHours - (totalDays * 24)
            remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
            totalMinutes = (totalSeconds - hoursInSeconds) / 60
            totalMinutes = math.floor(totalMinutes)
            timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(
                totalMinutes) \
                        + ' minutes'
            print(event)
            timeUntilEvent[event] = timeUntil
            # print(event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) + ' minutes')

    return timeUntilEvent

def updateSpecificEventTimer(event):
    event_times = read_event_times()
    timeUntilEvent = dict()
    currentTime = datetime.now()
    eventTime = event_times[event]
    if eventTime < currentTime:
        addedTime = timedelta(days=5, hours=4)
        eventTime = eventTime + addedTime
        print(event + ' is out of date, it was fixed')
        totalSeconds = eventTime - currentTime
        totalDays = totalSeconds.days
        totalSeconds = totalSeconds.total_seconds()

        remainingSeconds = (totalSeconds % hourToSeconds)
        hoursInSeconds = totalSeconds - remainingSeconds
        totalHours = hoursInSeconds / hourToSeconds
        totalHours = totalHours - (totalDays * 24)
        remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
        totalMinutes = (totalSeconds - hoursInSeconds) / 60
        totalMinutes = math.floor(totalMinutes)
        timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(
            totalMinutes) \
                    + ' minutes'
        timeUntilEvent[event] = timeUntil

    elif currentTime < eventTime:
        totalSeconds = eventTime - currentTime
        totalDays = totalSeconds.days
        totalSeconds = totalSeconds.total_seconds()

        remainingSeconds = (totalSeconds % hourToSeconds)
        hoursInSeconds = totalSeconds - remainingSeconds
        totalHours = hoursInSeconds / hourToSeconds
        totalHours = totalHours - (totalDays * 24)
        remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
        totalMinutes = (totalSeconds - hoursInSeconds) / 60
        totalMinutes = math.floor(totalMinutes)
        timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(
            totalMinutes) \
                    + ' minutes'
    return timeUntil

def timeUntilSpecificEvent(event)   :
    timeUntilEvent = updateSpecificEventTimer(event)
    return timeUntilEvent


def returnEventOptions():
    timeUntilEvent = updateEventTimers()
    eventOptions = ''
    for event in timeUntilEvent.keys():
        eventOptions += (', ' + event)
        print(eventOptions)
    eventOptions = eventOptions[1:]
    return eventOptions
