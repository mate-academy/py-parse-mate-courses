import requests
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin

from . import course as c
from .course import CourseType


BASE_MATE_ACADEMY = "https://mate.academy/"


@dataclass
class CourseParse:
    # response from main page mate academy
    page_soup: BeautifulSoup

    def course_detail_page(self, course_link: Tag) -> BeautifulSoup:
        """Get course detail page"""
        detail_link = urljoin(BASE_MATE_ACADEMY, course_link["href"])
        page = requests.get(detail_link).content
        page_soup = BeautifulSoup(page, "html.parser")

        return page_soup

    def prepare_course_data(
            self, course_soup: BeautifulSoup, course_detail: BeautifulSoup
    ) -> dict:
        course = {
            "name": course_soup.select_one(c.NAME).string,
            "short_description": course_soup.select_one(
                c.SHORT_DESCRIPTION
            ).string,
            "course_type": (
                CourseType.PART_TIME
                if "parttime" in course_detail.select_one(
                    c.COURSE_TYPE)["content"]
                else CourseType.FULL_TIME
            ),
            "num_modules": int(
                course_detail.select_one(c.NUM_MODULES).string.split()[0]
            ),
            "num_topics": int(
                course_detail.select_one(c.NUM_TOPICS).string.split()[0]
            ),
            "duration": course_detail.select_one(c.DURATION).string
        }
        return course

    def create_courses(self, course_soup: BeautifulSoup) -> list[c.Course]:
        """ Create 2 courses if exist for full-time/part-time """
        return [
            c.Course(
                **self.prepare_course_data(
                    course_soup,
                    self.course_detail_page(course_link)
                )
            )
            for course_link in course_soup.select(c.PART_FULL_LINKS)
        ]

    def get_all_courses(self) -> list:
        courses_card = self.page_soup.select(c.COURSES_CARD)
        courses = []
        for course in courses_card:
            courses.extend(self.create_courses(course))
        return courses


def get_all_courses() -> list[c.Course]:
    page = requests.get(BASE_MATE_ACADEMY).content
    page_soup = BeautifulSoup(page, "html.parser")
    return CourseParse(page_soup).get_all_courses()
