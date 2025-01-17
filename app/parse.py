from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from bs4.element import Tag


URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str

    def __str__(self) -> str:
        return (f"Course: {self.name}\nDescription: {self.short_description}\n"
                f"Duration: {self.duration}\n")


def get_course_info(card: Tag) -> Course:
    name = card.select_one(
        ".typography_landingH3__vTjok.ProfessionCard_title__fEWio.mb-12 > h3"
    ).text

    short_description = card.select_one(
        "p.typography_landingTextMain__Rc8BD.mb-32"
    ).text

    duration = card.select_one(
        ".typography_landing"
        "TextMain__Rc8BD.ProfessionCardTags_regularTag__dqOGj "
        "> span:last-child"
    ).text

    return Course(name, short_description, duration)


def get_all_courses() -> list[Course]:
    rsp = requests.get(URL)
    rsp.raise_for_status()
    soup = BeautifulSoup(rsp.content, "html.parser")

    cards = soup.select(".ProfessionCard_cardWrapper__2Q8_V")

    return [course for card in cards if (course := get_course_info(card))]


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
