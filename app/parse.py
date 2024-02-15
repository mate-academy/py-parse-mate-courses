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
    course_type: CourseType
    modules: int = None
    topics: int = None
    duration: int = None


def get_detail_info(url: str) -> dict:
    new_url = urljoin(BASE_URL, url)
    page = requests.get(new_url).content
    soup = BeautifulSoup(page, "html.parser")

    modules = soup.select_one(
        ".CourseModulesHeading_modulesNumber__UrnUh"
        "> .CourseModulesHeading_text__bBEaP"
    ).text.split()[0]
    topics = soup.select_one(
        ".CourseModulesHeading_topicsNumber__5IA8Z"
        "> .CourseModulesHeading_text__bBEaP"
    ).text.split()[0]
    duration = soup.select_one(
        ".CourseModulesHeading_courseDuration__qu2Lx"
        "> .CourseModulesHeading_text__bBEaP"
    ).text.split()[0]
    return {
        "modules": modules,
        "topics": topics,
        "duration": duration
    }


def get_single_unit_course(
        course_soup: BeautifulSoup,
        course_type: str
) -> Course:
    name = course_soup.select_one("h3").text
    description = course_soup.select_one(".mb-32").text

    choices = {
        "Власний темп": CourseType.PART_TIME,
        "Повний день": CourseType.FULL_TIME
    }
    if choices[course_type] == CourseType.PART_TIME:
        a = course_soup.find(
            "a", {"data-qa": "parttime-course-more-details-button"}
        )
        url = a.get("href")
    else:
        a = course_soup.find(
            "a", {"data-qa": "fulltime-course-more-details-button"}
        )
        url = a.get("href")

    return Course(
        name=name,
        short_description=description,
        course_type=choices[course_type],
        **get_detail_info(url),
    )


def get_unit_course(course_soup: BeautifulSoup) -> Course:
    course_types = [
        course_type.text
        for course_type in
        course_soup.select(".ButtonBody_buttonText__FMZEg")
    ]
    for url in course_soup.select("a.Button_secondary__DNIuD"):
        get_detail_info(url["href"])
    return [
        get_single_unit_course(course_soup, course_type)
        for course_type in course_types
    ]


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select("div.ProfessionCard_cardWrapper__JQBNJ")

    return [
        course
        for unit_course in courses
        for course in get_unit_course(unit_course)
    ]


if __name__ == "__main__":
    for course in get_all_courses():
        print(course)
