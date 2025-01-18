from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup, Tag

HOME_PAGE_URL = " https://mate.academy/"


def parse_attr(page: Tag, name: str, class_: str) -> Tag | ValueError:
    attr = page.find(name, class_)
    if attr is None:
        raise ValueError(f"Could not find attribute {name}")
    return attr


def parse_course_name(page: Tag) -> str | None:
    name = parse_attr(
        page,
        "a",
        "typography_landingH3__vTjok ProfessionCard_title__fEWio mb-12")
    return name.find("h3").text


def parse_course_description(page: Tag) -> str | None:
    description = parse_attr(
        page,
        "p",
        "typography_landingTextMain__Rc8BD mb-32")
    return description.text


def parse_course_duration(page: Tag) -> str | None:
    course_tags = parse_attr(
        page,
        "div",
        "ProfessionCard_professionTags__2iarD mb-24")
    duration = course_tags.find_all("span")[-1]
    return duration.text


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    response = requests.get(HOME_PAGE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    profession_cards = soup.find_all(
        "div",
        "ProfessionCard_cardWrapper__2Q8_V")

    return [Course(
        name=parse_course_name(profession_cards[card]),
        short_description=parse_course_description(profession_cards[card]),
        duration=parse_course_duration(profession_cards[card]))
        for card in range(len(profession_cards))]


if __name__ == "__main__":
    print(get_all_courses())
