from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    url: str
    modules: str
    topics: str

    def __str__(self) -> str:
        return (f"{self.name} | {self.short_description[:20]} ... | "
                f"{self.duration} | {self.modules} | {self.topics} | "
                f"{self.url}")


BASE_URL = "https://mate.academy/"


def get_url_soup(url: str) -> BeautifulSoup:
    """Get url content & raise exception if error.
    Return - html parsed BeautifulSoup object."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def load_detail(course: Course) -> list[str]:
    detail_marker = ".CourseModulesHeading_text__bBEaP"
    soup_course = get_url_soup(urljoin(BASE_URL, course.url))
    return [el.text for el in soup_course.select(detail_marker)[:2]]


def load_course(course_html: Tag) -> Course:
    name = course_html.select_one(".typography_landingH3__vTjok")
    course = Course(
        name=name.text,
        duration=course_html.select_one(".mb-24 > span").text,
        short_description=course_html.select_one(".mb-32").text,
        url=name.attrs["href"].split("?")[0],
        modules="",
        topics="",
    )
    course.modules, course.topics = load_detail(course)
    return course


def get_all_courses() -> list[Course]:
    soup = get_url_soup(BASE_URL)
    courses_html = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [load_course(course_html) for course_html in courses_html]


if __name__ == "__main__":
    all_courses = get_all_courses()
    [print(course) for course in all_courses]
