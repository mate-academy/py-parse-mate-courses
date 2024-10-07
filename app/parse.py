from dataclasses import dataclass
from pprint import pprint

from bs4 import BeautifulSoup
import requests

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    tags = course_soup.find_all(["span"])
    duration = None
    for tag in tags:
        if "місяц" in tag.text:
            duration = tag.text
            break

    return Course(
        name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
        short_description=course_soup.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    courses_list = []
    page_url = BASE_URL

    page = requests.get(page_url).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    courses_list.extend(
        [parse_single_course(course_soup) for course_soup in courses]
    )
    return courses_list


def main() -> None:
    pprint(get_all_courses())


if __name__ == "__main__":
    main()
