import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"
SELECTOR_NAME = ".ProfessionCard_title__Zq5ZY"
SELECTOR_DESCRIPTION = ".typography_landingTextMain__Rc8BD.mb-32"
SELECTOR_DURATION = ".ProfessionCardTags_regularTag__yTc6K"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one(SELECTOR_NAME).text,
        short_description=course_soup.select_one(SELECTOR_DESCRIPTION).text,
        duration=course_soup.select_one(SELECTOR_DURATION).text,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course) for course in course_elements]
