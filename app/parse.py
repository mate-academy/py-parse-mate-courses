from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: BeautifulSoup) -> Course:
    name = course.select_one("h3").text
    short_description = course.select_one("p.mb-32").text
    duration = [
        span.text
        for span in course.select(
            ".ProfessionCard_professionTags__2iarD p span"
        )
    ][-1]

    return Course(
        name=name,
        short_description=short_description,
        duration=duration
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")

    mate_courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")

    results = [parse_single_course(course) for course in mate_courses]

    return results


if __name__ == "__main__":
    get_all_courses()
