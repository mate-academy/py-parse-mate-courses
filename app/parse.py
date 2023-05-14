from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup
import json


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_course(course_dict: dict) -> Course:
    name = course_dict['nameShort({"domain":"ua","lang":"uk"})']
    is_part_time = "Вечірній" in name.split()
    course_type = (
        CourseType.PART_TIME if is_part_time else CourseType.FULL_TIME
    )
    return Course(name, course_dict["description"], course_type)


def get_all_courses() -> [Course]:
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    script = soup.select_one("#__NEXT_DATA__")
    content = dict(json.loads(script.text))["props"]["apolloState"]
    courses = [val for key, val in content.items() if key.startswith("Course")]

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    courses = get_all_courses()
    print(courses)
