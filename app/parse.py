from dataclasses import dataclass
from enum import Enum
import re

import requests
from bs4 import BeautifulSoup as Bs

BASE_URL = "https://mate.academy/"


class HTTPResponseError(Exception):
    def __init__(self, url: str, status_code: int) -> None:
        super().__init__(
            f"Error getting page: {url}, status code: {status_code}"
        )


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


# ProfessionCard_cardWrapper__JQBNJ
def get_main_page(timeout: int = 10) -> str:
    try:
        response = requests.get(BASE_URL, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        raise HTTPResponseError(BASE_URL, response.status_code) from error


def get_all_courses() -> [Course]:
    content = get_main_page()
    soup = Bs(content, "html.parser")

    all_courses_info = soup.find_all(
        "div", class_=re.compile("ProfessionCard_cardWrapper.*")
    )

    list_of_courses = []
    for course_info in all_courses_info:
        name = course_info.find(
            "a", class_=re.compile("ProfessionCard_title.*")
        ).text

        short_description = course_info.find_all(
            "p", class_=re.compile("typography_landingTextMain.*")
        )[-1].text

        flex = course_info.find_all(
            "a", attrs={"data-qa": "fx-course-details-button"}
        )
        full = course_info.find_all(
            "a", attrs={"data-qa": "fulltime-course-more-details-button"}
        )
        if full:
            list_of_courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.FULL_TIME,
                )
            )
        if flex:
            list_of_courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    course_type=CourseType.PART_TIME,
                )
            )

    return list_of_courses


def main() -> None:
    get_all_courses()


if __name__ == "__main__":
    main()
