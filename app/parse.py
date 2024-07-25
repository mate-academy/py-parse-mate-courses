import csv
from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/en"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "flex"


@dataclass
class Course:
    name: str
    short_description: str
    course_types: list[str]


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    courses = soup.find_all("div", class_="ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []

    for course in courses:
        course_name = course.find(
            "a",
            class_="typography_landingH3__vTjok "
                   "ProfessionCard_title__Zq5ZY mb-12"
        )
        course_description = course.find(
            "p",
            class_="typography_landingTextMain__Rc8BD mb-32"
        )
        course_types = [
            type_.get_text().lower().replace(" ", "-")
            for type_ in course.find_all(
                "span",
                "ButtonBody_buttonText__FMZEg"
            )
        ]

        course_obj = Course(
            name=course_name.text,
            short_description=course_description.text,
            course_types=course_types,
        )
        all_courses.append(course_obj)

    with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "description", "types"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        for course in all_courses:
            writer.writerow(
                [
                    course.name, course.short_description,
                    ", ".join(course.course_types)
                ]
            )

    return all_courses


if __name__ == "__main__":
    courses = get_all_courses()
    print(f"Find {len(courses)} courses")
