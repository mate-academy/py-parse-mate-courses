from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag
import httpx


URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    name = course.select_one("h3").text
    description = course.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text
    duration = course.select_one(
        ".ProfessionCardTags_regularTag__dqOGj:last-child span"
    ).text

    return Course(
        name=name,
        short_description=description,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    with httpx.Client() as client:
        content = client.get(URL).content
        soup = BeautifulSoup(content, "html.parser")
        courses_murkup = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
        return [parse_single_course(course) for course in courses_murkup]
