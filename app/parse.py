import requests


from dataclasses import dataclass
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_course_info_soup(course_soup: BeautifulSoup) -> BeautifulSoup:
    course_info_page = course_soup.select_one("a")["href"]
    course_url = urljoin(BASE_URL, course_info_page)

    course_page = requests.get(course_url).content

    course_info_soup = BeautifulSoup(course_page, "html.parser")

    return course_info_soup


def parse_course_name(course_soup: BeautifulSoup) -> Course:
    return Course(
        name=course_soup.select_one("a")["title"],
        short_description=get_course_info_soup(course_soup).find(
            class_="typography_landingTextMain__Rc8BD"
                   " SalarySection_aboutProfession__1VFHK"
        ).text,
        duration=get_course_info_soup(course_soup).find_all(
            class_="ComparisonTable_cell__RNsyU ComparisonTable_highl"
                   "ightCell__IpyWZ typography_newLandingH6__Av9tT"
        )[12].text
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    base_page_soup = BeautifulSoup(page, "html.parser")
    courses = base_page_soup.select(
        ".HeaderCoursesDropdown_coursesListItem__36tl_"
    )
    return [parse_course_name(course_soup) for course_soup in courses]


if __name__ == "__main__":
    get_all_courses()
