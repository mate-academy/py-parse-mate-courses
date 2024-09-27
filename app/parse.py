from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


BASE_URL = "https://mate.academy/"


def get_single_course(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one("h3").text,
        short_description=course.select_one(".mb-32").text,
        duration=f"{course.select_one('.mb-24').text.split('+')[0]}+ months"
    )


def get_all_courses() -> list[Course]:
    base_page = requests.get(BASE_URL).content
    soup = BeautifulSoup(base_page, "html.parser")
    course_tag = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [get_single_course(course) for course in course_tag]


if __name__ == "__main__":
    get_all_courses()
