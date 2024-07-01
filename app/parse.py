import csv
from dataclasses import dataclass, astuple
from enum import Enum
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://mate.academy"
COURSES_OUTPUT_CSV_PATH = "courses.csv"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"

    def __str__(self):
        return self.value


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def fetch_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def parse_single_course(course_card: BeautifulSoup, course_type: CourseType) -> Course:
    title_pattern = re.compile(r'ProfessionCard_title__[a-zA-Z0-9]{5}')
    description_pattern = re.compile(r'typography_landingTextMain__[a-zA-Z0-9]{5}')

    name = course_card.find(class_=title_pattern).get_text(strip=True)
    short_description = course_card.find(class_=description_pattern).find_next('p').get_text(strip=True)

    return Course(
        name=name,
        short_description=short_description,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    all_courses = []
    soup = fetch_html(BASE_URL)
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course in courses:
        full_time_link = course.find("a", {"data-qa": "fulltime-course-more-details-button"})
        part_time_link = course.find("a", {"data-qa": "fx-course-details-button"})

        if full_time_link:
            all_courses.append(parse_single_course(course, CourseType.FULL_TIME))
        if part_time_link:
            all_courses.append(parse_single_course(course, CourseType.PART_TIME))

    return all_courses


def save_courses_to_csv(courses: list[Course], filename: str) -> None:
    print(f"Saving {len(courses)} courses to {filename}...")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Name", "Short Description", "Course Type"]
        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)
        for course in courses:
            row = astuple(course)
            row = [str(value) if isinstance(value, Enum) else value for value in row]
            writer.writerow(row)
    print(f"Courses saved to {filename}.")


def main():
    courses = get_all_courses()
    if courses:
        save_courses_to_csv(courses, COURSES_OUTPUT_CSV_PATH)
    else:
        print("No courses found.")


if __name__ == "__main__":
    main()
