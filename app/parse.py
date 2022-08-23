from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    type: CourseType
    modules: int
    topics: int
    duration: int


def parse_single_course(
        education_soup: BeautifulSoup,
        optional_soup: BeautifulSoup,
        course_type
) -> dict:
    return dict(
        name=education_soup.select_one(".typography_landingH3__vTjok").text,
        short_description=education_soup.select_one(
            ".CourseCard_flexContainer__dJk4p > p"
        ).text,
        type=course_type,
        modules=int(
            optional_soup.select_one(
                ".CourseModulesHeading_modulesNumber__GNdFP > p"
            ).text.split()[0]
        ),
        topics=int(
            optional_soup.select_one(
                ".CourseModulesHeading_topicsNumber__PXMnR > p"
            ).text.split()[0]
        )
    )


def parse_course_detail(education_soup: BeautifulSoup, course_type) -> Course:
    course_detail = education_soup.select_one("a")["href"]
    course_url = urljoin(BASE_URL, course_detail)
    page = requests.get(course_url).content
    soup = BeautifulSoup(page, "html.parser")

    course = parse_single_course(education_soup, soup, course_type)

    if course["type"] == CourseType.FULL_TIME:
        course["duration"] = soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H > p"
        ).text.split()[0]
    else:
        course["duration"] = None

    return Course(
        name=course["name"],
        short_description=course["short_description"],
        type=course["type"],
        modules=course["modules"],
        topics=course["topics"],
        duration=course["duration"],
    )


def parse_courses_list(all_curses: BeautifulSoup, course_type) -> list[Course]:
    return [
        parse_course_detail(education_soup, course_type)
        for education_soup in all_curses
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    full_time_courses = soup.select(
        "#full-time .CourseCard_cardContainer__7_4lK"
    )
    part_time_courses = soup.select(
        "#part-time .CourseCard_cardContainer__7_4lK"
    )

    return parse_courses_list(full_time_courses, CourseType.FULL_TIME)\
        + parse_courses_list(part_time_courses, CourseType.PART_TIME)


def main():
    print(get_all_courses())


if __name__ == "__main__":
    main()
