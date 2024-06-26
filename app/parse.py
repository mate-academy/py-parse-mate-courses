from dataclasses import dataclass
from enum import Enum

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://mate.academy/"


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
    duration: str


def get_course_details(url: str) -> dict:
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    course_modules = soup.select(".CourseModulesHeading_text__bBEaP")[0].text
    course_topics = soup.select(".CourseModulesHeading_text__bBEaP")[1].text
    course_duration = soup.select(".CourseModulesHeading_text__bBEaP")[2].text

    return {
        "modules": course_modules,
        "topics": course_topics,
        "duration": course_duration
    }


def create_course(course_soup: Tag, full_time: bool = False) -> Course:
    course_type = CourseType.PART_TIME
    course_url = (
        URL[:-1] + course_soup.select_one("a[data-qa^='part']").attrs["href"]
    )

    if full_time:
        course_type = CourseType.FULL_TIME
        course_url = (
            URL[:-1] + course_soup.select_one("a[data-qa^='fu']").attrs["href"]
        )

    details = get_course_details(course_url)

    return Course(
        name=course_soup.select_one("h3").text,
        short_description=course_soup.select_one(".mb-32").text,
        course_type=course_type,
        modules=details["modules"],
        topics=details["topics"],
        duration=details["duration"]
    )


def get_all_courses() -> list[Course]:
    page = requests.get(URL).content
    soup = BeautifulSoup(page, "html.parser")

    soup_courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    all_courses = []

    for course in soup_courses:
        all_courses.append(create_course(course))

        if course.select_one("a[data-qa^='full']"):
            all_courses.append(create_course(course, full_time=True))

    return all_courses
