import csv
from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_all_courses() -> list[Course]:
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        courses = soup.find_all(
            "div",
            class_="ProfessionCard_cardWrapper__JQBNJ"
        )
    except Exception as e:
        print(f"Error parsing the webpage: {e}")
        return []

    all_courses = []

    for course in courses:
        try:
            course_name = course.find(
                "a",
                class_="typography_landingH3__vTjok "
                       "ProfessionCard_title__Zq5ZY mb-12",
            ).get_text()

            course_description = course.find(
                "p", class_="typography_landingTextMain__Rc8BD mb-32"
            ).get_text()

            course_types = [
                type_.get_text().lower().replace(" ", "-")
                for type_ in course.find_all(
                    "span", class_="ButtonBody_buttonText__FMZEg"
                )
            ]

            for course_type in course_types:
                if course_type == "full-time":
                    single_course = Course(
                        name=course_name,
                        short_description=course_description,
                        course_type=CourseType.FULL_TIME,
                    )
                else:
                    single_course = Course(
                        name=course_name,
                        short_description=course_description,
                        course_type=CourseType.PART_TIME,
                    )
                all_courses.append(single_course)
        except AttributeError as e:
            print(f"Error extracting course details: {e}")
            continue

    try:
        with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["name", "description", "type"]
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            for course in all_courses:
                writer.writerow(
                    [
                        course.name,
                        course.short_description,
                        course.course_type.value
                    ]
                )
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

    return all_courses


if __name__ == "__main__":
    courses = get_all_courses()
    print(f"Find {len(courses)} courses")
