import logging
import sys
from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules: int
    topics: int
    duration: int


BASE_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)8s]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    courses = []

    name = course_soup.select_one("h3").text
    short_description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text

    full_time_course_type = course_soup.select_one(
        "[data-qa='fulltime-course-more-details-button']"
    )
    part_time_course_type = course_soup.select_one(
        "[data-qa='parttime-course-more-details-button']"
    )

    course_link = BASE_URL + course_soup.select_one("a")["href"]
    page = requests.get(course_link).content
    page_soup = BeautifulSoup(page, "html.parser")

    modules = int(
        page_soup.select_one(
            ".CourseModulesHeading_modulesNumber__GNdFP p"
        ).text.split(" ")[0]
    )
    topics = int(
        page_soup.select_one(
            ".CourseModulesHeading_topicsNumber__PXMnR p"
        ).text.split(" ")[0]
    )
    duration = int(
        page_soup.select_one(
            ".CourseModulesHeading_courseDuration__f_c3H p"
        ).text.split(" ")[0]
    )

    if full_time_course_type:
        courses.append(
            Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.FULL_TIME,
                modules=modules,
                topics=topics,
                duration=duration,
            )
        )

    if part_time_course_type:
        courses.append(
            Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.PART_TIME,
                modules=modules,
                topics=topics,
                duration=duration,
            )
        )

    return courses


def get_all_courses() -> list[Course]:
    all_courses = []

    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")

    courses = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses.extend(
        [course for soup in courses for course in parse_single_course(soup)]
    )

    return all_courses


get_all_courses()
