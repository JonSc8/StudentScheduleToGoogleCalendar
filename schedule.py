from selenium import webdriver
from course import Course

class Schedule:
    
    def __init__(self, schedule_table):
        self.courses = self.create_schedule(schedule_table)
    
    def create_schedule(self, schedule_table):
        print("Creating schedule")
        courses_info = []
        for course in schedule_table.find_elements_by_xpath(".//tr")[3:-1]:
            tmp = []
            for td in course.find_elements_by_xpath(".//td"):
                td = td.text.split("\n")
                if len(td) == 1:
                    tmp.append(td[0])
                else:
                    tmp.append(td[0])
                    tmp.append(td[1])
            if(len(tmp) == 11):
                courses_info.append(tmp)
        
        course_object_list = []
        for course in courses_info:
            new_course = Course(course[1], course[0], course[4], course[6], course[7], course[8], course[9], course[10])
            course_object_list.append(new_course)

        return course_object_list
