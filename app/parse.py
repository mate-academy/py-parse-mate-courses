import logging
import sys
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_single_types_course(soup_course: Tag) -> tuple[Course, Course]:
    name = soup_course.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY.mb-12"
    ).text
    short_description = soup_course.select_one(
        ".typography_landingTextMain__Rc8BD.mb-32"
    ).text

    logging.info(f"Parsing {name} course")

    full_time = Course(
        name=name,
        short_description=short_description,
        course_type=CourseType.FULL_TIME,
    )

    part_time = Course(
        name=name,
        short_description=short_description,
        course_type=CourseType.PART_TIME,
    )

    logging.info("Parsing part-time details")

    if soup_course.select_one(
            "[data-qa='fulltime-course-more-details-button']"
    ):
        logging.info("Parsing full-time details")

    return full_time, part_time


def get_all_courses() -> list[Course]:
    logging.info("Starting parsing")
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    soup_courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for soup_course in soup_courses:
        all_courses.extend(parse_single_types_course(soup_course))

    return all_courses
