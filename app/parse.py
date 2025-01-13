import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_count: int = None
    topics_count: int = None


def parse_single_course(course_element: Tag) -> Course:
    name = course_element.select_one("h3").text.strip()
    short_description = course_element.select_one(
        ".typography_landingTextMain__Rc8BD"
    ).text.strip()
    duration = course_element.select(
        ".typography_landingTextMain__Rc8BD span"
    )[-1].text.strip()

    modules_count = len(course_element.select(".module-selector"))
    topics_count = len(course_element.select(".topic-selector"))

    return Course(name, short_description, duration,
                  modules_count, topics_count)


def get_all_courses() -> list[Course]:
    content = requests.get("https://mate.academy/")
    content.raise_for_status()

    soup = BeautifulSoup(content.text, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [
        parse_single_course(course_element)
        for course_element in course_elements
    ]
