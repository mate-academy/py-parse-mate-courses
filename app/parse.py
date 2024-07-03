from dataclasses import dataclass
from enum import Enum

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


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    name = course_soup.select_one("h3").text
    short_description = course_soup.select_one("p.mb-32").text
    course_button_soup = course_soup.select_one(
        ".ProfessionCard_buttons__a0o60"
    )
    course_type_buttons = [button.text for button in course_button_soup]

    courses_list = []

    for button in course_type_buttons:
        if button == "Повний день":
            single_course = Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.FULL_TIME
            )
            courses_list.append(single_course)
        elif button == "Гнучкий графік":
            single_course = Course(
                name=name,
                short_description=short_description,
                course_type=CourseType.PART_TIME
            )
            courses_list.append(single_course)
    return courses_list


def parse_course_page(page_soup: BeautifulSoup) -> list[Course]:
    course_soups = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = []
    for course_soup in course_soups:
        all_courses.extend(parse_single_course(course_soup))
    return all_courses


def scrape_course_page(url: str) -> list[Course]:
    response = requests.get(url)
    page_soup = BeautifulSoup(response.text, "html.parser")
    return parse_course_page(page_soup)


def get_all_courses() -> list[Course]:
    return scrape_course_page(BASE_URL)
