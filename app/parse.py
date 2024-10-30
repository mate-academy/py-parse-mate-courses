from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

MATE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_single_course(tag: Tag) -> Course:
    return Course(
        name=tag.find("h3").text,
        short_description=tag.find("p", class_="mb-32").text,
        duration=tag.find(
            "p", class_="ProfessionCardTags_regularTag__yTc6K"
        ).text
    )


def get_all_courses() -> list[Course]:
    session = requests.Session()
    soup = BeautifulSoup(session.get(MATE_URL).text, "html.parser")
    tags = soup.find_all("div", {"data-qa": "profession-card"})
    return [get_single_course(tag) for tag in tags]
