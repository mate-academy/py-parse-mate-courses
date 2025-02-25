from abc import ABC, abstractmethod
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from typing import List


BASE_URL = "https://mate.academy"


# --- Entities ---
@dataclass
class Course:
    name: str
    short_description: str
    duration: str


# --- Repositories ---
class CoursesRepository(ABC):
    @abstractmethod
    def get_all_courses(self) -> List[Course]:
        pass


class HtmlFetcher:
    def fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text


class MateAcademyHtmlParser:
    def parse(self, html: str) -> List[Course]:
        soup = BeautifulSoup(html, "html.parser")
        courses = []
        for course_card in soup.select("a.ProfessionCard_cardWrapper__BCg0O"):
            name = course_card.select_one("h3.ProfessionCard_title__m7uno").text.strip()
            description = course_card.select_one(
                "p.ProfessionCard_description__K8weo"
            ).text.strip()
            duration = course_card.select_one(
                "p.ProfessionCard_duration__13PwX"
            ).text.strip()
            courses.append(
                Course(
                    name=name,
                    short_description=description,
                    duration=duration,
                )
            )
        return courses


class WebCoursesRepository(CoursesRepository):
    def __init__(
        self,
        base_url: str,
        html_fetcher: HtmlFetcher,
        parser: MateAcademyHtmlParser,
    ) -> None:
        self.base_url = base_url
        self.html_fetcher = html_fetcher
        self.parser = parser

    def get_all_courses(self) -> List[Course]:
        html = self.html_fetcher.fetch(self.base_url)
        return self.parser.parse(html)


# --- Adapters  ---
class HtmlFetcher:
    def fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text


class MateAcademyHtmlParser:
    def parse(self, html: str) -> List[Course]:
        soup = BeautifulSoup(html, "html.parser")
        courses = []
        for course_card in soup.select("a.ProfessionCard_cardWrapper__BCg0O"):
            name = course_card.select_one("h3.ProfessionCard_title__m7uno").text.strip()
            description = course_card.select_one(
                "p.ProfessionCard_description__K8weo"
            ).text.strip()
            duration = course_card.select_one(
                "p.ProfessionCard_duration__13PwX"
            ).text.strip()
            courses.append(
                Course(
                    name=name,
                    short_description=description,
                    duration=duration,
                )
            )
        return courses


# --- Use Cases  ---
class GetAllCourses:
    def __init__(self, repository: CoursesRepository) -> None:
        self.repository = repository

    def execute(self) -> List[Course]:
        return self.repository.get_all_courses()


# --- Frameworks & Drivers ---
def get_all_courses() -> List[Course]:
    html_fetcher = HtmlFetcher()
    parser = MateAcademyHtmlParser()
    repository = WebCoursesRepository(BASE_URL, html_fetcher, parser)
    use_case = GetAllCourses(repository)

    courses = use_case.execute()
    print(courses)
    return courses


if __name__ == "__main__":
    get_all_courses()
