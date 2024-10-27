from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_number_from_months_text(text: str) -> str:
    return text.split(" ")[0][:-1]


def parse_single_course(course: Tag) -> Course:
    name = course.select_one("a h3").text
    description = course.find_all("p", recursive=False)[0].text
    duration = get_number_from_months_text(
        course.select_one("div > p:last-child > span").text)

    return Course(name=name, short_description=description, duration=duration)


def get_all_courses() -> list[Course]:
    landing_page = requests.get(BASE_URL).content

    soup = BeautifulSoup(landing_page, "html.parser")

    courses_cards = soup.select('div[data-qa="profession-card"]')

    return [parse_single_course(course_card) for course_card in courses_cards]
