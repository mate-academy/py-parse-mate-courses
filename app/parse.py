from dataclasses import dataclass

from bs4 import BeautifulSoup, ResultSet
import requests


BASE_URL = "https://www.mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def fetch_page(url: str) -> BeautifulSoup:
    page = requests.get(url)
    if page.status_code != 200:
        raise Exception(page.status_code)
    return BeautifulSoup(page.content, "html.parser")


def extract_courses(soup: BeautifulSoup) -> ResultSet:
    section = soup.find("section", {"id": "all-courses"})
    return section.find_all("div", class_="ProfessionCard_cardWrapper__JQBNJ")


def parse_course(course_element: BeautifulSoup) -> Course:
    name = course_element.select_one(".typography_landingH3__vTjok")
    short_description = course_element.find(
        "p", class_="typography_landingTextMain__Rc8BD mb-32"
    ).text
    duration = course_element.find_all(
        "p", class_="typography_landingTextMain__Rc8BD ProfessionCardTags_regularTag__yTc6K"
    )[-1].text

    return Course(
        name=name.text,
        short_description=short_description,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    soup = fetch_page(BASE_URL)
    courses = []
    for course in extract_courses(soup):
        courses.append(parse_course(course))
    return courses
