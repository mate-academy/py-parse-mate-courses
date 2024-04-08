import requests
from urllib.parse import urljoin
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
from typing import List, Tuple

from source import (
    COURSE_TYPES_PATH,
    COURSE_DETAIL_LINK_PATH,
    MODULES_PATH,
    TOPICS_PATH,
    DURATION_PATH,
    MATE_URL,
    COURSES_PATH
)


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


def get_all_courses() -> list[Course]:
    all_courses = []
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(COURSES_PATH)
    course_parser = CourseParser()
    for course in courses:
        all_courses.extend(course_parser.parse_single_course(course))
    return all_courses


class CourseParser:

    def parse_single_course(
            self,
            course_soup: BeautifulSoup
    ) -> tuple[Course] | tuple[Course, Course]:
        if "data-qa" in course_soup.attrs:
            course_types = self.get_course_type(course_soup=course_soup)
            modules, topics, duration = self.get_moduls_topics_and_duration(
                course_soup=course_soup
            )
            if len(course_types) == 1:
                return (Course(
                    name=course_soup.select_one("a").text,
                    short_description=course_soup.select_one(".mb-32").text,
                    course_type=course_types[0],
                    modules=modules,
                    topics=topics,
                    duration=duration
                ),)
            else:
                return (Course(
                    name=course_soup.select_one("a").text,
                    short_description=course_soup.select_one(".mb-32").text,
                    course_type=course_types[0],
                    modules=modules,
                    topics=topics,
                    duration=duration
                ), Course(
                    name=course_soup.select_one("a").text,
                    short_description=course_soup.select_one(".mb-32").text,
                    course_type=course_types[1],
                    modules=modules,
                    topics=topics,
                    duration=duration
                ))

    @staticmethod
    def get_course_type(course_soup: BeautifulSoup) -> List[CourseType]:
        course_types = course_soup.select(COURSE_TYPES_PATH)
        if len(course_types) == 2:
            return [CourseType.FULL_TIME, CourseType.PART_TIME]
        else:
            return [CourseType.PART_TIME]

    @staticmethod
    def get_moduls_topics_and_duration(
            course_soup: BeautifulSoup
    ) -> Tuple[int, int, int]:
        course_detail_link = course_soup.select(
            COURSE_DETAIL_LINK_PATH
        )[0]["href"]
        page = requests.get(
            urljoin(MATE_URL, course_detail_link)
        ).content
        soup = BeautifulSoup(page, "html.parser")
        modules = int(
            "".join(filter(str.isdigit, soup.select_one(MODULES_PATH).text))
        )
        topics = int(
            "".join(filter(str.isdigit, soup.select_one(TOPICS_PATH).text))
        )
        duration = int(
            "".join(filter(str.isdigit, soup.select_one(DURATION_PATH).text)))
        return modules, topics, duration
