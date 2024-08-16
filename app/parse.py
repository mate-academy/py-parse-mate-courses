from dataclasses import dataclass
from enum import Enum
import requests
from bs4 import BeautifulSoup


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


@dataclass
class FullTimeCourse(Course):
    pass


@dataclass
class PartTimeCourse(Course):
    pass


BASE_URL = "https://mate.academy/"


def get_detailed_information() -> list[str]:
    links = []
    detail = requests.get(BASE_URL).content
    soup = BeautifulSoup(detail, "html.parser")
    for link_element in soup.select("a.typography_landingH3__vTjok"):
        href = link_element.get("href")
        full_link = BASE_URL + href
        links.append(full_link)
    return links


def get_courses_detail(url: str) -> BeautifulSoup:
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        print(f"Failed to retrieve {url}")
        return None


def parse_single_course(course_soup: BeautifulSoup) -> list[Course]:
    if not course_soup:
        return []

    title = course_soup.select_one(
        ".typography_landingH1__RS6qi"
    ).text.strip()
    description = course_soup.select_one(
        ".typography_landingTextMain__Rc8BD.color-gray-60"
    ).text.strip()

    courses = []

    courses.append(
        PartTimeCourse(
            name=title,
            short_description=description,
            course_type=CourseType.PART_TIME,
        )
    )
    courses.append(
        FullTimeCourse(
            name=title,
            short_description=description,
            course_type=CourseType.FULL_TIME,
        )
    )

    return courses


def get_all_courses() -> list[Course]:
    links = get_detailed_information()
    courses = []

    for link in links:
        course_soups = parse_single_course(get_courses_detail(link))
        courses.extend(course_soups)

    return courses


if __name__ == "__main__":
    courses = get_all_courses()
