from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"
INFO_COURSES = ".ProfessionCard_cardWrapper__JQBNJ"
PARAGRAPHS_DURATION_DESCRIPTION = ".typography_landingTextMain__Rc8BD"
PARAGRAPH_NAME = ".typography_landingH3__vTjok > h3"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(product_soup: BeautifulSoup) -> Course:
    paragraphs_duration_and_description = product_soup.select(
        PARAGRAPHS_DURATION_DESCRIPTION
    )
    name = product_soup.select_one(
        PARAGRAPH_NAME
    ).text
    short_description = paragraphs_duration_and_description[1].text
    duration = paragraphs_duration_and_description[0].text.split("•")[0]

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    products = soup.select(INFO_COURSES)

    return [parse_single_course(product_soup) for product_soup in products]


print(get_all_courses())
