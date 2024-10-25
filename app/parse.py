from dataclasses import dataclass

import requests
from bs4 import Tag, BeautifulSoup


MATE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: int = None
    topics: int = None


def get_detail_course_info(course_detail_url: str) -> tuple[int, int]:
    detail_page = requests.get(MATE_URL + course_detail_url[1:]).content
    soup = BeautifulSoup(detail_page, "html.parser")

    program = soup.select_one(
        "section.profession-page-container > "
        "div.CourseProgram_content__tvxzY"
    )
    modules = len(program.select("div.CourseProgram_modules__GA_PJ > ul > li"))
    topics = int(program.select_one(".FactBlock_factNumber__d_8nn").text)
    return modules, topics


def get_course(course_tag: Tag) -> Course:
    course = Course(
        name=course_tag.select_one("h3").text,
        short_description=course_tag.select_one("div + p").text,
        duration=course_tag.select("p > span")[-1].text,
    )
    course.modules, course.topics = get_detail_course_info(course_tag.select_one("div > a")["href"])

    return course


def get_all_courses() -> list[Course]:
    site = requests.get(MATE_URL).content
    soup = BeautifulSoup(site, "html.parser")

    course_blocks = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [get_course(tag) for tag in course_blocks]


if __name__ == "__main__":
    print(get_all_courses())
