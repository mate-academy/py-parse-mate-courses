from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/#all-courses"

@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_course(course):
    return Course(
        name=course.select_one(".ProfessionCard_title__m7uno").text,
        short_description=course.select_one(".ProfessionCard_description__K8weo").text,
        duration=course.select_one(".ProfessionCard_duration__13PwX").text

    )


def get_all_courses() -> list[Course]:
    page_html = requests.get(BASE_URL).text
    soup_page = BeautifulSoup(page_html, "html.parser")
    courses = soup_page.select(".ProfessionsListSectionTemplate_card__ZNsgf")
    return [parse_course(course) for course in courses]

print(get_all_courses())