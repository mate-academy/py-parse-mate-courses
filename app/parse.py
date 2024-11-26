import requests
import csv

from dataclasses import dataclass, astuple, fields

from bs4 import BeautifulSoup, Tag

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


FIELDS_LIST = [field.name for field in fields(Course)]


def parse_single_course(soup: Tag) -> Course:
    return Course(
        name=soup.select_one("a.ProfessionCard_title__fEWio > h3").text,
        short_description=soup.select_one(
            ".ProfessionCard_professionTags__2iarD + "
            "p.typography_landingTextMain__Rc8BD"
        ).text,
        duration=soup.select_one(
            "p.ProfessionCardTags_regularTag__dqOGj:last-child span"
        ).text
    )


def get_all_courses() -> list[Course]:
    try:
        text = requests.get(BASE_URL).content
    except requests.exceptions.RequestException as e:
        print(e)
    soup = BeautifulSoup(text, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [parse_single_course(course) for course in courses]


def write_to_csv(courses: list[Course]) -> None:
    with open("courses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(FIELDS_LIST)
        writer.writerows(astuple(course) for course in courses)


def main() -> None:
    write_to_csv(get_all_courses())


if __name__ == "__main__":
    main()
