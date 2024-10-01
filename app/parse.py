from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def map_course(card_selector: Tag) -> Course:
    name = card_selector.a.text
    base_selector = "p.typography_landingTextMain__Rc8BD"
    short_description = card_selector.select_one(
        base_selector + ".mb-32"
    ).text
    duration = card_selector.select_one(
        base_selector
        + ".ProfessionCard_subtitle__K1Yp6.mb-24"
    ).span.text

    course = Course(
        name=name,
        short_description=short_description,
        duration=duration
    )

    return course


def get_all_courses() -> list[Course]:
    page = requests.get(url=URL).text
    soup = BeautifulSoup(markup=page, features="html.parser")
    cards_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    courses = [
        map_course(card_selector)
        for card_selector in cards_soup
    ]

    return courses
