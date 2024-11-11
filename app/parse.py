from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_soup(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup


def get_data_from_soup(soup):
    all_courses = soup.select("div.ProfessionCard_cardWrapper__JQBNJ")
    return [
        {
            "name": course.select_one("a.typography_landingH3__vTjok > h3").text,
            "short_description": course.select_one(
                "div.ProfessionCard_cardWrapper__JQBNJ > "
                "p.typography_landingTextMain__Rc8BD"
            ).text,
            "duration": (
                course.select_one(
                    "div.ProfessionCard_professionTags__kCD1H > p:last-child"
                ).text
            ),
        }
        for course in all_courses
    ]


def create_class_objects(data_from_soup):
    return [
        Course(
            name=data["name"],
            short_description=data["short_description"],
            duration=data["duration"],
        )
        for data in data_from_soup
    ]


def get_all_courses() -> list[Course]:
    soup = get_soup("https://mate.academy")
    data_from_soup = get_data_from_soup(soup)
    list_of_courses = create_class_objects(data_from_soup)
    return list_of_courses

