from typing import Union, List

import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from enum import Enum


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType


def parse_course_type(
        course_soup: Tag
) -> Union[CourseType, List[CourseType], None]:
    full_time = course_soup.select_one(
        ".Button_brandSecondary__DXhVs.Button_large__rIMVg"
        ".Button_button__bwept.Button_fullWidth___Ft6W"
    )
    part_time = course_soup.select_one(
        ".Button_brandPrimary__uJ_Nl.Button_large__rIMVg"
        ".Button_button__bwept.Button_fullWidth___Ft6W"
    )

    if full_time and part_time:
        return [CourseType.FULL_TIME, CourseType.PART_TIME]
    elif full_time:
        return CourseType.FULL_TIME
    elif part_time:
        return CourseType.PART_TIME


def get_single_course(soup_page: Tag, type_course: CourseType) -> Course:
    return Course(
        name=soup_page.select_one("h3").text,
        short_description=soup_page.select_one(
            "p.typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        course_type=type_course
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")
    all_cards = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    all_courses = [get_single_course(soup_card, CourseType.FULL_TIME) for soup_card in all_cards]
    all_courses.extend([get_single_course(soup_card, CourseType.PART_TIME) for soup_card in all_cards])
    return all_courses


if __name__ == "__main__":
    courese = get_all_courses()
    for course in courese:
        print(course)
