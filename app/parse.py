from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


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


def get_duration(soup: BeautifulSoup) -> str:
    duration = soup.find_all(
        "p",
        "typography_landingTextMain__Rc8BD CourseModulesHeading_text__bBEaP"
    )[2].text.split()[0] + " months"
    return duration


def get_topics(soup: BeautifulSoup) -> int:
    topics = int(soup.find_all(
        "p",
        "typography_landingTextMain__Rc8BD CourseModulesHeading_text__bBEaP"
    )[1].text.split()[0])
    return topics


def get_modules(soup: BeautifulSoup) -> int:
    modules = int(soup.find_all(
        "p",
        "typography_landingTextMain__Rc8BD CourseModulesHeading_text__bBEaP"
    )[0].text.split()[0])
    return modules


def get_short_description(soup: BeautifulSoup) -> str:
    short_description = soup.find_all(
        "p", "typography_landingTextMain__Rc8BD color-gray-60"
    )[0].text
    return short_description


def get_detail_page(name: str) -> BeautifulSoup:
    url_name = name.lower().split()[0]
    if url_name == "recruiter":
        url_name = "recruitment"
    if "-" in name:
        url_name = url_name.replace("-", "")
    if "/" in name:
        url_name = url_name.replace("/", "-")
    if "flex" in name:
        url_name += "-parttime"
    detail_url = urljoin(BASE_URL, f"/courses/{url_name}?")
    page = requests.get(detail_url).content
    soup = BeautifulSoup(page, "html.parser")
    return soup


def single_course(course: BeautifulSoup) -> Course:
    name = course.select_one(".ButtonBody_buttonText__FMZEg").text
    if "flex" in name:
        course_type = CourseType.PART_TIME
    else:
        course_type = CourseType.FULL_TIME
    detail_page = get_detail_page(name)
    return Course(
        name=name,
        course_type=course_type,
        short_description=get_short_description(detail_page),
        modules=get_modules(detail_page),
        topics=get_topics(detail_page),
        duration=get_duration(detail_page)
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    soup_courses = soup.select(".DropdownCoursesList_coursesListItem__5fXRO")
    courses = [single_course(course) for course in soup_courses]
    return courses


print(get_all_courses())
