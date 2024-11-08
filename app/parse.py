import csv
from dataclasses import dataclass, fields, astuple

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy/"
OUTPUT_CSV_PATH = "course.csv"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(page_soup: BeautifulSoup) -> Course:
    return Course(
        name=page_soup.select_one("h3").text,
        short_description=page_soup.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=page_soup.select_one(
            "p.typography_landingTextMain__Rc8BD."
            "ProfessionCardTags_regularTag__yTc6K:last-of-type > "
            "span:last-of-type"
        ).text
    )


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL).content
    page_soup = BeautifulSoup(page, "html.parser")
    courses = page_soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [parse_single_course(course_soup) for course_soup in courses]


def write_products_to_csv(courses: [Course]) -> None:
    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main() -> None:
    courses = get_all_courses()
    write_products_to_csv(courses)


if __name__ == "__main__":
    main()
