import httpx

from bs4 import BeautifulSoup
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin


URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    duration: str
    modules: int
    topics: int


all_courses = []


def get_course_type(course_type: str) -> CourseType:
    if course_type.lower() in ["full-time", "повний день"]:
        return CourseType.FULL_TIME

    return CourseType.PART_TIME


def get_detail_page_soup(
        course_block: BeautifulSoup,
        client: httpx.Client
) -> BeautifulSoup:
    detail_url = course_block.select_one("a.Button_large__rIMVg").get("href")
    page = client.get(urljoin(URL, detail_url))

    return BeautifulSoup(page.content, "html.parser")


def get_module_count(page_soup: BeautifulSoup) -> int:
    modules_count = page_soup.select_one(
        ".CourseModulesHeading_modulesNumber__UrnUh"
    ).text.split()[0]

    return int(modules_count)


def get_topic_count(page_soup: BeautifulSoup) -> int:
    topics_count = page_soup.select_one(
        ".CourseModulesHeading_topicsNumber__5IA8Z"
    ).text.split()[0]

    return int(topics_count)


def parse_single_course(
        course_block: BeautifulSoup,
        client: httpx.Client
) -> None:
    type_list = [
        button.text
        for button in course_block.select(".ButtonBody_buttonText__FMZEg")
    ]
    detail_page_soup = get_detail_page_soup(course_block, client)

    for course_type in type_list:
        course = Course(
            name=course_block.select_one("h3").text,
            short_description=course_block.select_one(
                "p.typography_landingTextMain__Rc8BD.mb-32"
            ).text,
            course_type=get_course_type(course_type),
            duration=course_block.select_one("p > span").text,
            modules=get_module_count(detail_page_soup),
            topics=get_topic_count(detail_page_soup),
        )
        all_courses.append(course)


def parse_home_page_courses(
        page_soup: BeautifulSoup,
        client: httpx.Client
) -> None:
    course_blocks = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    for course_block in course_blocks:
        parse_single_course(course_block, client)


def get_all_courses() -> list[Course]:
    with httpx.Client() as client:
        page = client.get(URL).content
        soup = BeautifulSoup(page, "html.parser")
        parse_home_page_courses(soup, client)

    return all_courses


if __name__ == "__main__":
    print(get_all_courses())
