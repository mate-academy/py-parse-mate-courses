from dataclasses import dataclass
from enum import Enum
from typing import List

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
    duration_in_months: int


class MateCoursesScraper:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    @staticmethod
    def get_page_soup(url: str) -> BeautifulSoup:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")

    @staticmethod
    def prettify_num_field(field: Tag) -> int:
        return int(field.text.split()[0])

    def get_single_course(
        self, url: str, course_type: CourseType, course_soup: Tag
    ) -> Course:
        course_details_soup = self.get_page_soup(url).select_one(
            ".CourseModulesHeading_headingGrid__ynoxV"
        )

        return Course(
            name=course_soup.select_one(".ProfessionCard_title__Zq5ZY").text,
            short_description=course_soup.select_one(".mb-32").text,
            course_type=course_type,
            modules_count=self.prettify_num_field(
                course_details_soup.select_one(
                    ".CourseModulesHeading_modulesNumber__UrnUh > p"
                )
            ),
            topics_count=self.prettify_num_field(
                course_details_soup.select_one(
                    ".CourseModulesHeading_topicsNumber__5IA8Z > p"
                )
            ),
            duration_in_months=self.prettify_num_field(
                course_details_soup.select_one(
                    ".CourseModulesHeading_courseDuration__qu2Lx > p"
                )
            ),
        )

    def parse_course(self, course_soup: Tag) -> List[Course]:
        flex_course_details_url = self.base_url + course_soup.select_one(
            "[data-qa=fx-course-details-button]"
        ).get("href")

        courses = [
            self.get_single_course(
                flex_course_details_url, CourseType.PART_TIME, course_soup
            ),
        ]

        if course_soup.select_one(
            "[data-qa=fulltime-course-more-details-button]"
        ):
            fulltime_course_derails_url = (
                self.base_url
                + course_soup.select_one(
                    "[data-qa=fulltime-course-more-details-button]"
                ).get("href")
            )

            courses.append(
                self.get_single_course(
                    fulltime_course_derails_url,
                    CourseType.FULL_TIME,
                    course_soup,
                )
            )

        return courses

    def scrape_all_courses(self) -> list[Course]:
        page_soup = self.get_page_soup(self.base_url)

        all_courses = []
        courses_soup = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

        for course in courses_soup:
            all_courses.extend(self.parse_course(course))

        return all_courses


def get_all_courses() -> list[Course]:
    scraper = MateCoursesScraper(BASE_URL)

    return scraper.scrape_all_courses()


if __name__ == "__main__":
    get_all_courses()
