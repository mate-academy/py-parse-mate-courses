import csv
from dataclasses import dataclass, fields, astuple
from bs4 import BeautifulSoup
from enum import Enum

import requests

URL = "https://mate.academy"
OUTPUT_CSV_FILE = "mate-courses.csv"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


COURSES_FIELDS = [field.name for field in fields(Course)]


def parse_singe_course(course: BeautifulSoup) -> Course:
    name = course.select_one("a.Button_transparentLight__JIwOr")["title"]
    course_type = CourseType.PART_TIME \
        if "flex" in name else CourseType.FULL_TIME

    course_link = course.select_one("a.Button_transparentLight__JIwOr")["href"]
    page_detail = requests.get(f"https://mate.academy{course_link}").content
    soup_detail = BeautifulSoup(page_detail, "html.parser")
    description = soup_detail.select_one(
        "div.AboutProfessionSection_secondaryBlock__rVdvd > "
        ".typography_landingTextMain__Rc8BD")
    return Course(
        name=name,
        short_description=description.text,
        course_type=course_type.value,
    )


def get_courses() -> [Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_courses = []
    for course in soup.select("li.DropdownCoursesList_coursesListItem__5fXRO"):
        all_courses.append(parse_singe_course(course))
    return all_courses


def write_courses_to_csv(courses: [Course]) -> None:
    with open(OUTPUT_CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(COURSES_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main() -> None:
    courses = get_courses()
    write_courses_to_csv(courses)


if __name__ == "__main__":
    main()
