import requests
from urllib.parse import urljoin
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup

MATE_URL = "https://mate.academy/"


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
    page = requests.get(MATE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [parse_single_course(course) for course in courses]


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    if "data-qa" in course_soup.attrs:
        course_type = get_course_type(course_soup)
        modules, topics, duration = get_moduls_topics_and_duration(course_soup)
        return Course(
            name=course_soup.select_one("a").text,
            short_description=course_soup.select_one(".mb-32").text,
            course_type=course_type,
            modules=modules,
            topics=topics,
            duration=duration
        )
    else:
        pass


def get_course_type(course_soup: BeautifulSoup) -> CourseType:
    course_types = course_soup.select(".ProfessionCard_buttons__a0o60 > a")
    if len(course_types) == 2:
        return CourseType.FULL_TIME
    else:
        return CourseType.PART_TIME


def get_moduls_topics_and_duration(course_soup: BeautifulSoup) -> tuple:
    course_detail_link = course_soup.select(
        ".ProfessionCard_buttons__a0o60 > a"
    )[0]["href"]
    page = requests.get(urljoin(MATE_URL, course_detail_link)).content
    soup = BeautifulSoup(page, "html.parser")
    modules = "".join(filter(str.isdigit, soup.select_one(
        ".CourseModulesHeading_text__bBEaP"
    ).text))
    topics = "".join(filter(str.isdigit, soup.select_one(
        ".CourseModulesHeading_topicsNumber__5IA8Z"
    ).text))
    duration = "".join(filter(str.isdigit, soup.select_one(
        ".CourseModulesHeading_courseDuration__qu2Lx"
    ).text))
    return int(modules), int(topics), int(duration)


if __name__ == "__main__":
    print(get_all_courses())
