from dataclasses import dataclass
from enum import Enum
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    modules_count: int
    topics_count: int
    duration: str


class ScrapeMateCourses:
    def __init__(self) -> None:
        self.list_of_courses = []

    def get_all_courses(self) -> list[Course]:
        page = requests.get(BASE_URL).content
        soup = BeautifulSoup(page, "html.parser")
        courses_direction = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

        for course_direction_soup in courses_direction:
            self.scrape_course_direction(course_direction_soup)

        return self.list_of_courses

    def scrape_course_direction(self, course_direction_soup: Tag) -> None:
        course_types = course_direction_soup.select(
            ".ButtonBody_buttonText__FMZEg"
        )
        course_detail_soup = self.get_detail_page_soup(
            course_direction_soup=course_direction_soup
        )

        for course_type in course_types:
            self.scrape_single_course(
                course_direction_soup=course_direction_soup,
                course_detail_soup=course_detail_soup,
                course_type=course_type.text,
            )

    def scrape_single_course(
            self,
            course_direction_soup: Tag,
            course_detail_soup: Tag,
            course_type: str
    ) -> None:
        self.list_of_courses.append(
            Course(
                name=self.get_name(course_direction_soup),
                short_description=self.get_short_description(
                    course_direction_soup
                ),
                course_type=self.get_course_type(course_type),
                modules_count=self.get_modules_count(course_detail_soup),
                topics_count=self.get_topics_count(course_detail_soup),
                duration=self.get_duration(course_detail_soup),
            )
        )

    @staticmethod
    def get_name(course_direction_soup: Tag) -> str:
        return course_direction_soup.select_one("h3").text

    @staticmethod
    def get_short_description(course_direction_soup: Tag) -> str:
        return course_direction_soup.select_one(".mb-32").text

    @staticmethod
    def get_course_type(course_type: str) -> CourseType:
        if course_type == "Повний день":
            return CourseType.FULL_TIME
        return CourseType.PART_TIME

    @staticmethod
    def get_modules_count(course_detail_soup: Tag) -> int:
        return int(
            course_detail_soup.select_one(
                ".CourseModulesHeading_modulesNumber__UrnUh "
                "> p.CourseModulesHeading_text__bBEaP"
            ).text.split()[0]
        )

    @staticmethod
    def get_topics_count(course_detail_soup: Tag) -> int:
        return int(
            course_detail_soup.select_one(
                ".CourseModulesHeading_topicsNumber__5IA8Z "
                "> p.CourseModulesHeading_text__bBEaP"
            ).text.split()[0]
        )

    @staticmethod
    def get_duration(course_detail_soup: Tag) -> str:
        return course_detail_soup.select_one(
            ".CourseModulesHeading_topicsNumber__5IA8Z "
            "> p.CourseModulesHeading_text__bBEaP"
        ).text.split()[0]

    @staticmethod
    def get_detail_page_soup(course_direction_soup: Tag) -> BeautifulSoup:
        course_detail_page = requests.get(
            urljoin(
                BASE_URL,
                course_direction_soup.select_one(
                    ".typography_landingH3__vTjok"
                )
                .get("href"),
            )
        ).content

        return BeautifulSoup(course_detail_page, "html.parser")
