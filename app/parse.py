from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course_soup: Tag) -> Course:
    name = course_soup.select_one("a.ProfessionCard_title__Zq5ZY > h3").text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32").text
    duration = course_soup.select("span")[-2].text
    return Course(name, short_description, duration)


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course) for course in courses]
