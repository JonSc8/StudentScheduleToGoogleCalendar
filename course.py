import re
from datetime import datetime

class Course:
    def __init__(self, name, further_details, instructor, week_days, time, location, start_date, end_date):
        self.name = name
        self.further_details = further_details
        self.instructor = instructor
        self.week_days = week_days
        self.time = time
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
    
    def get_name(self):
        return self.name
    
    def get_further_details(self):
        details = self.instructor + ", " + self.further_details
        return details
    
    def get_location(self):
        return self.location
    
    def get_week_days(self):
        days = self.week_days.upper()
        return re.sub(" ", ",", days)
    
    def get_course_end_date(self):
        date_object = datetime.strptime(self.end_date, '%m/%d/%y')

        date = str(date_object).split(" ")
        date = date[0]
        date = re.sub("-", "", date)
        return date
    
    def get_start_date_time(self):
        start_datetime = self.start_date + " " + self.get_start_time()
        datetime_object = datetime.strptime(start_datetime, '%m/%d/%y %H:%M')
        return datetime_object.isoformat("T")
    
    def get_end_date_time(self):
        end_datetime = self.start_date + " " + self.get_end_time()
        datetime_object = datetime.strptime(end_datetime, '%m/%d/%y %H:%M')
        return datetime_object.isoformat("T")
    
    def get_start_time(self):
        time = self.time.split("-")
        start_time = ""

        if "am" in time[0]:
            start_time = re.sub("am", "", time[0])
        else:
            tmp = time[0].split(":")
            start_time = str(int(tmp[0]) + 12) + ":" + tmp[1]
            start_time = re.sub("pm", "", start_time)
        
        return start_time
    
    def get_end_time(self):
        time = self.time.split("-")
        end_time = ""

        if "am" in time[1]:
            end_time = re.sub("am", "", time[1])
        else:
            tmp = time[1].split(":")
            if "12" in tmp[0]:
                end_time = re.sub("pm", "", time[1])
            else:
                end_time = str(int(tmp[0]) + 12) + ":" + tmp[1]
                end_time = re.sub("pm", "", end_time)

        return end_time