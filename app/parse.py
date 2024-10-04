import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_one_course(courses_soup: BeautifulSoup) -> Course:
    return Course(
        name=courses_soup.select_one("h3").text,
        short_description=courses_soup.select_one(".mb-32").text,
        duration=courses_soup.select_one(".mb-24 > span").text,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [get_one_course(courses_soup) for courses_soup in courses]
