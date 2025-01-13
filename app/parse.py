from dataclasses import dataclass, fields
import requests
from bs4 import BeautifulSoup


HOME_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


QUOTE_FIELDS = [field.name for field in fields(Course)]


def parse_single_quote(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one("h3").text,
        short_description=course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=course.select_one(
            ".ProfessionCardTags_regularTag__dqOGj:last-child span"
        ).text,
    )


def get_all_courses() -> list[Course]:
    text = requests.get(HOME_URL).content
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    recived_course = [parse_single_quote(course) for course in courses]
    return recived_course


if __name__ == "__main__":
    get_all_courses()
