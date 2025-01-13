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
    try:
        name = course_element.select_one("h3").text.strip()
    except AttributeError:
        name = "N/A"

    try:
        short_description = course_element.select_one(
            ".typography_landingTextMain__Rc8BD"
        ).text.strip()
    except AttributeError:
        short_description = "No description available"

    try:
        duration = course_element.select(
            ".typography_landingTextMain__Rc8BD span"
        )[-1].text.strip()
    except (AttributeError, IndexError):
        duration = "Duration not available"

    modules_count = len(course_element.select(".module-selector")) if course_element.select(".module-selector") else 0
    topics_count = len(course_element.select(".topic-selector")) if course_element.select(".topic-selector") else 0

    return Course(name, short_description, duration, modules_count, topics_count)


def get_all_courses() -> list[Course]:
    content = requests.get("https://mate.academy/")
    content.raise_for_status()

    soup = BeautifulSoup(content.text, "html.parser")
    course_elements = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [
        parse_single_course(course_element)
        for course_element in course_elements
    ]
