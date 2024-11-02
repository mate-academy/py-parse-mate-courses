import requests
from bs4 import BeautifulSoup

from dataclasses import dataclass


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    count_topics: int = None


def parse_single_course(course: BeautifulSoup) -> Course:
    course_obj = Course(
        name=course.select_one("h3").text,
        short_description=course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=[
            sub_text.text
            for sub_text in course.select(
                ".ProfessionCardTags_regularTag__yTc6K > span"
            )
        ][-1],
    )

    course_obj.count_topics = get_count_of_topics(
        course.select_one(
            "a[data-qa='flex-course-more-details-button']"
        )["href"]
    )

    return course_obj


def open_detail_course_page(sub_link: str) -> BeautifulSoup:
    page = requests.get(BASE_URL + sub_link).content
    return BeautifulSoup(page, "html.parser")


def get_count_of_topics(sub_link: str) -> int:
    detail_page = open_detail_course_page(sub_link)

    return int(
        detail_page.select_one(
            ".FactBlock_factIconBlock__cgzql.CourseProgram_card__Myw3S."
            "CourseProgram_purple__STsuM > p.FactBlock_factNumber__d_8nn"
        ).text)


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course) for course in courses]
