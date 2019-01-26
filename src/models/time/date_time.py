# import pytz
import datetime
import src.models.time.constants as TimeConstants
import re
import random


class DateTime(object):
    # defining the time zone object.
    # tzone = pytz.timezone(TimeConstants.TIMEZONE)

    @staticmethod
    def get_time():
        # return datetime.datetime.now(tz=DateTime.tzone)
        # giving the timezone is ideal but having an issue while saving to
        # mongoDB the time zone is getting lost
        return datetime.datetime.now()

    @staticmethod
    def get_time_str1():
        # in the format 201808211020, %Y%m%m%H%M
        return DateTime.get_time().strftime('%Y%m%d%H%M')

    @staticmethod
    def get_time_html(time_str):
        # in the format 2018-10-01T14:58, %Y-%m-%dT%H:%M
        return datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M')

    @staticmethod
    def this_week():
        end = datetime.datetime.now()
        week_today = end.weekday()
        week_offset = TimeConstants.weekday.get(week_today)
        end_no_time = datetime.datetime.strptime(end.strftime('%Y-%m-%d'), '%Y-%m-%d')
        # the strptime re-write is to avoid the time and retain the date
        start = end_no_time - datetime.timedelta(days=week_offset)
        return start, end

    # @staticmethod
    # def this_year():
    #     end = datetime.datetime.now()
    #     week_today = end.weekday()
    #     week_offset = TimeConstants.weekday.get(week_today)
    #     end_no_time = datetime.datetime.strptime(end.strftime('%Y-%m-%d'), '%Y-%m-%d')
    #     # the strptime re-write is to avoid the time and retain the date
    #     start = end_no_time - datetime.timedelta(days=week_offset)
    #     return start, end

    @staticmethod
    def last_week():
        week_start, time_now = DateTime.this_week()
        start = week_start - datetime.timedelta(days=7)
        end = week_start
        return start, end

    @staticmethod
    def this_month():
        end = datetime.datetime.now()
        date_num = end.day
        # remove time from the date
        # it will be better to remove time with the replace time option.
        date_no_time = datetime.datetime.strptime(end.strftime('%Y-%m-%d'), '%Y-%m-%d')
        # todays date minus the date number gives the begining of the month
        start = date_no_time - datetime.timedelta(days=date_num-1)
        return start, end

    @staticmethod
    def last_month():
        month_start, time_today = DateTime.this_month()
        end = month_start
        last_month_end = end - datetime.timedelta(days=1)
        date_num = last_month_end.day
        date_no_time = datetime.datetime.strptime(end.strftime('%Y-%m-%d'), '%Y-%m-%d')
        start = date_no_time - datetime.timedelta(days=date_num)
        return start, end

    @staticmethod
    def get_time_diff_no_sec(uptime, downtime ):
        # takes the start and end time and returns the string value of the difference
        dur = uptime - downtime
        # this output will be in the format '1 day, 0:00:00.513212'
        # omitting the microsecond and the milli second from the output

    @staticmethod
    def snooze(duration):
        snz_map = dict(week=1, month=4, month_3=12)
        return datetime.datetime.now() + datetime.timedelta(snz_map[duration])

    @staticmethod
    def random_time(start=None):
        # returns a random date in last 6 months, add time to the randomizer
        end = datetime.datetime.now()
        if not start:
            delta_day = 180
            start = end - datetime.timedelta(days=delta_day)
        delta_day = (end-start).days
        event_time = random.randrange(delta_day - 1)
        event_time = start + datetime.timedelta(days=event_time)
        return event_time

    @staticmethod
    def convert_str_to_time(str_time):
        # currently the input should be in 2018-08-15 21:59 format
        # add dynamic detection and convert here
        return datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M')

    @staticmethod
    def this_year():
        end = datetime.datetime.now()
        start = datetime.datetime.strptime(str(end.year), '%Y')
        return start, end









