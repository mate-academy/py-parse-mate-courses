import csv

import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, astuple

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_single_course(soup: Tag) -> Course:
    return (Course(
        name=soup.select_one("a.ProfessionCard_title__fEWio > h3").text,
        short_description=soup.select_one(
            ".ProfessionCard_professionTags__2iarD + "
            "p.typography_landingTextMain__Rc8BD"
        ).text,
        duration=soup.select_one(
            ".ProfessionCardTags_regularTag__dqOGj:last-child span"
        ).text
    ))


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [parse_single_course(course) for course in courses]


def save_courses_to_csv(quotes: list[Course], output_csv_path: str) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "short_description", "duration"])
        writer.writerows([astuple(quote) for quote in quotes])
