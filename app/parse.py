from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: BeautifulSoup) -> Course:
    return Course(
        name=course.select_one(
            "h1[data-qa='profession-title']"
        ).text.split(":")[0],
        short_description=course.select_one(
            "p.typography_landingTextMain__Rc8BD."
            "SalarySection_aboutProfession__1VFHK"
        ).text,
        duration=course.select_one(
            ".ComparisonTable_tableBody__W5hzV.mb-24 "
            "> div:nth-of-type(7) "
            "> div:nth-of-type(2)"
        ).text
    )


def get_courses_urls() -> list[str]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_courses = [
        course["href"].split("/courses/")[-1]
        for course in soup.select(
            ".HeaderCoursesDropdown_dropdownWrapper__3Agil "
            "a[href*='/courses/']"
        )
    ]
    return all_courses


def get_all_courses() -> list[Course]:
    courses_urls = get_courses_urls()
    all_courses_info = []
    for course in courses_urls:
        page = requests.get(BASE_URL + "/courses/" + course).content
        soup = BeautifulSoup(page, "html.parser")
        course = parse_single_course(soup)
        all_courses_info.append(course)

    return all_courses_info


if __name__ == "__main__":
    print(get_all_courses())
