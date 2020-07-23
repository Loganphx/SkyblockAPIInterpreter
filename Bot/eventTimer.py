# date in yyyy/mm/dd format
import math
from datetime import timedelta, datetime

hourToSeconds = 3600
minutesToSeconds = 60
TravellingZooSummer = '2020-07-24 21:55:00.00000'
SpookyFestival = '2020-07-21 20:35:00.00000'
TravellingZooWinter = '2020-07-22 07:55:00.00000'
WinterIsland = '2020-07-23 04:35:00.00000'
SeasonOfJerry = '2020-07-23 12:15:00.00000'
NewYearCelebration = '2020-07-23 13:55:00.00000'
OldEvent = '2020-07-20 12:55:00.00000'
currentTime = datetime.now()
TZS_Datetime = datetime.strptime(TravellingZooSummer, '%Y-%m-%d %H:%M:%S.%f')
SF_Datetime = datetime.strptime(SpookyFestival, '%Y-%m-%d %H:%M:%S.%f')
TZW_Datetime = datetime.strptime(TravellingZooWinter, '%Y-%m-%d %H:%M:%S.%f')
WI_Datetime = datetime.strptime(WinterIsland, '%Y-%m-%d %H:%M:%S.%f')
SOJ_Datetime = datetime.strptime(WinterIsland, '%Y-%m-%d %H:%M:%S.%f')
NYC_Datetime = datetime.strptime(NewYearCelebration, '%Y-%m-%d %H:%M:%S.%f')
Old_Datetime = datetime.strptime(OldEvent, '%Y-%m-%d %H:%M:%S.%f')
events = {'Travelling Zoo Summer': TZS_Datetime, 'Spooky Festival': SF_Datetime, 'Travelling Zoo Winter': TZW_Datetime,
          'Winter Island': WI_Datetime, 'Season of Jerry': SOJ_Datetime, 'New Year Celebration': NYC_Datetime,
          'Old Event': Old_Datetime}

# Comparing the dates will return
# either True or False
timeUntilEvent = dict()
for event in events:
    eventTime = events[event]
    if (eventTime < currentTime):
        addedTime = timedelta(days=5, hours=4)
        eventTime = eventTime + addedTime
        events[event] = eventTime
        print(event + ' is out of date, it was fixed')
        totalSeconds = eventTime - currentTime
        totalDays = totalSeconds.days
        totalSeconds = totalSeconds.total_seconds()

        remainingSeconds = (totalSeconds % hourToSeconds)
        hoursInSeconds = totalSeconds - remainingSeconds
        totalHours = (hoursInSeconds) / hourToSeconds
        totalHours = totalHours - (totalDays * 24)
        remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
        totalMinutes = ((totalSeconds - hoursInSeconds)) / 60
        totalMinutes = math.floor((totalMinutes))
        timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) \
                    + ' minutes'
        timeUntilEvent[event] = timeUntil
        # print('Next occurance is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) + ' minutes')


    elif (currentTime < eventTime):
        totalSeconds = eventTime - currentTime
        totalDays = totalSeconds.days
        totalSeconds = totalSeconds.total_seconds()

        remainingSeconds = (totalSeconds % hourToSeconds)
        hoursInSeconds = totalSeconds - remainingSeconds
        totalHours = (hoursInSeconds) / hourToSeconds
        totalHours = totalHours - (totalDays * 24)
        remainingMinutes = (hoursInSeconds - remainingSeconds) % 60
        totalMinutes = ((totalSeconds - hoursInSeconds)) / 60
        totalMinutes = math.floor((totalMinutes))
        timeUntil = event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) \
                    + ' minutes'
        print(event)
        timeUntilEvent[event] = timeUntil
        # print(event + ' is in ' + str(totalDays) + ' days, ' + str(totalHours) + ' hours, ' + str(totalMinutes) + ' minutes')


def timeUntilSpecificEvent(event):
    return timeUntilEvent[event]


def returnEventOptions():
    eventOptions = ''
    for event in events.keys():
        eventOptions += (', ' + event)
        print(eventOptions)
    eventOptions = eventOptions[1:]
    return eventOptions