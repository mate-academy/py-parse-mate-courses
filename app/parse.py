from dataclasses import dataclass
import re
import requests
from bs4 import BeautifulSoup
from typing import List

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: int


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    duration_text_element = course_soup.select_one(".mb-24")
    duration_number = (
        int(re.search(r"\d+", duration_text_element.text).group())
        if duration_text_element
        else 0
    )
    name_element = course_soup.select_one(".ProfessionCard_title__Zq5ZY")
    short_description_element = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    )

    return Course(
        name=name_element.text if name_element else "Unknown",
        short_description=short_description_element.text
        if short_description_element
        else "No description",
        duration=duration_number,
    )


def get_all_courses() -> List[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course) for course in courses]


if __name__ == "__main__":
    print(get_all_courses())
