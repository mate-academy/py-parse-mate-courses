import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str

BASE_URL = "https://mate.academy/"


def parse_single_course(soup: BeautifulSoup) -> Course:
    return Course(
        name=soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=soup.find(
            "p", {"class": "typography_landingTextMain__Rc8BD mb-32"}
        ).get_text(strip=True),
        duration=soup.select_one(
            ".ProfessionCardTags_regularTag__yTc6K > span"
        ).text
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    course_element = soup.select_one(
        ".ProfessionsListSection_cardsWrapper___Zpyd"
    )
    courses = course_element.find_all(
        "div", {"data-qa": "profession-card"}
    )
    all_courses = []
    for course in courses:
        all_courses.append(parse_single_course(course))
    return all_courses
