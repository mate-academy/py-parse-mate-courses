import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(product_soup: Tag) -> Course:
    course_type = CourseType.FULL_TIME
    name = product_soup.select_one(".typography_landingH3__vTjok").text
    if name.split()[-1] == "Вечірній":
        course_type = CourseType.PART_TIME

    return Course(
        name=name,
        short_description=product_soup.select_one(
            ".CourseCard_flexContainer__dJk4p"
        ).text,
        course_type=course_type
    )


def get_all_courses() -> list[Course]:
    base_url = "https://mate.academy/"

    page = requests.get(base_url).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".CourseCard_cardContainer__7_4lK")

    return [parse_single_course(course) for course in courses]
