from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(course: Tag) -> Course:

    return Course(
        name=course.select_one("a.typography_landingH3__vTjok h3").text,
        short_description=course.find(
            "p", class_="typography_landingTextMain__Rc8BD mb-32").get_text(),
        duration=course.select(
            "p.typography_landingTextMain__Rc8BD.ProfessionCardTags_regularTag__dqOGj")[-1].
        find("span").text,
    )


def get_all_courses() -> list[Course]:
    pass
