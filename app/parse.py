from dataclasses import dataclass

import requests
from bs4 import Tag, BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


BASE_URL = "https://mate.academy/"


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.find("h3").text,
        short_description=course.select(
            ".typography_landingTextMain__Rc8BD"
        )[-1].text,
        duration=course.select("span")[-2].text,
    )


def get_soup_of_page(url: str, session: requests.Session) -> BeautifulSoup:
    response = session.get(url)
    return BeautifulSoup(response.content, features="html.parser")


def get_all_courses() -> list[object]:
    session = requests.Session()
    soup = get_soup_of_page(BASE_URL, session)
    list_courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [parse_single_course(course) for course in list_courses]


if __name__ == "__main__":
    print(get_all_courses())
