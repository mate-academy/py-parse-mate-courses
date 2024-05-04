from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration: str


all_courses = []


def get_course_type(course_type: str) -> CourseType:
    if course_type == "Повний день":
        return CourseType.FULL_TIME
    return CourseType.PART_TIME


def get_name(course_direction_soup: Tag) -> str:
    return course_direction_soup.select_one("h3").text


def get_short_description(course_direction_soup: Tag) -> str:
    return course_direction_soup.select_one(".mb-32").text


def get_modules_count(course_detail_soup: Tag) -> int:
    return int(
        course_detail_soup.select_one(
            ".CourseModulesHeading_modulesNumber__UrnUh "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text.split()[0]
    )


def get_topics_count(course_detail_soup: Tag) -> int:
    return int(
        course_detail_soup.select_one(
            ".CourseModulesHeading_topicsNumber__5IA8Z "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text.split()[0]
    )


def get_duration(course_detail_soup: Tag) -> str:
    return course_detail_soup.select_one(
        ".CourseModulesHeading_topicsNumber__5IA8Z "
        "> p.CourseModulesHeading_text__bBEaP"
    ).text.split()[0]


def parse_single_course(
    course_direction_soup: Tag, course_detail_soup: Tag, course_type: str
) -> None:
    all_courses.append(
        Course(
            name=get_name(course_direction_soup),
            short_description=get_short_description(course_direction_soup),
            course_type=get_course_type(course_type),
            modules_count=get_modules_count(course_detail_soup),
            topics_count=get_topics_count(course_detail_soup),
            duration=get_duration(course_detail_soup),
        )
    )


def get_detail_page_soup(course_direction_soup: Tag) -> BeautifulSoup:
    course_detail_page = requests.get(
        urljoin(
            BASE_URL,
            course_direction_soup.select_one(
                ".typography_landingH3__vTjok"
            ).get("href"),
        )
    ).content

    return BeautifulSoup(course_detail_page, "html.parser")


def parse_course_direction(course_direction_soup: Tag) -> None:
    course_types = course_direction_soup.select(
        ".ButtonBody_buttonText__FMZEg"
    )
    course_detail_soup = get_detail_page_soup(
        course_direction_soup=course_direction_soup
    )

    for course_type in course_types:
        parse_single_course(
            course_direction_soup=course_direction_soup,
            course_detail_soup=course_detail_soup,
            course_type=course_type.text,
        )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses_direction = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course_direction_soup in courses_direction:
        parse_course_direction(course_direction_soup)

    return all_courses


if __name__ == "__main__":
    get_all_courses()
