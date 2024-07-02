from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def get_all_courses() -> list[Course]:
    url = "https://mate.academy/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    courses = []
    course_elements = soup.select('[data-qa="profession-card"]')

    course_type = None
    for element in course_elements:
        name = element.select_one("h3").text
        short_description = element.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text
        buttons = element.select("span[itemprop='name']")
        for button in buttons:
            button_text = button.text.strip()
            if "Повний день" in button_text:
                course_type = CourseType.FULL_TIME
            elif "Гнучкий графік" in button_text:
                course_type = CourseType.PART_TIME
            if course_type:
                course_data = Course(
                    name=name,
                    short_description=short_description,
                    course_type=course_type
                )
                courses.append(course_data)

    return courses


for course in get_all_courses():
    print(course)
