from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_page_content() -> BeautifulSoup:
    """Get and parse HTML content from mate.academy website."""
    response = requests.get(BASE_URL)
    return BeautifulSoup(response.content, "html.parser")


def parse_course(card: Tag) -> Course:
    """Extract course information from a course card."""
    name = card.select_one("h3").text.strip()
    short_description = card.select_one(
        "p[class*='typography_landingTextMain__Rc8BD mb-32']"
    ).text.strip()

    tags = card.select("p[class*='ProfessionCardTags_regularTag__']")
    duration = next(
        tag.text.strip()
        for tag in tags
        if tag.text.strip()[0].isdigit()
    )

    return Course(name, short_description, duration)


def get_all_courses() -> list[Course]:
    """Get list of all courses from mate.academy website."""
    page_content = get_page_content()
    course_cards = page_content.select(
        "div[class*='ProfessionCard_cardWrapper__']"
    )

    return [parse_course(card) for card in course_cards]


if __name__ == "__main__":
    print(get_all_courses())
