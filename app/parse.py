from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(courses: BeautifulSoup) -> [Course]:
    return Course(
        name=courses.select_one("h3").text,
        short_description=courses.select_one(".mb-32").text,
        duration=courses.select_one(".mb-24").text.split("•")[0]
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [parse_single_course(course) for course in courses]
