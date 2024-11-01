from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_course(course: Tag) -> Course:
    return Course(
        name=course.select_one(".ProfessionCard_title__Zq5ZY > h3").text,
        short_description=(
            course.select_one(".typography_landingTextMain__Rc8BD.mb-32").text
        ),
        duration=(
            course.select(
                ".ProfessionCardTags_regularTag__yTc6K"
                ".ProfessionCardTags_regularTag__yTc6K"
            )[-1].text
        )
    )

def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = [
        get_course(course)
        for course
        in soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    ]

    return courses
