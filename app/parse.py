from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:
    name = course.select_one("h3").text.strip()
    short_description = course.select(
        ".typography_landingTextMain__Rc8BD"
    )[-1].text
    duration = course.select(
        ".typography_landingTextMain__Rc8BD"
    )[1].text

    return Course(
        name=name, short_description=short_description, duration=duration
    )


def get_all_courses() -> list[Course]:
    content = requests.get(BASE_URL).content
    soup = BeautifulSoup(content, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [parse_single_course(course) for course in courses]


def main() -> None:
    print(get_all_courses())


if __name__ == "__main__":
    main()
