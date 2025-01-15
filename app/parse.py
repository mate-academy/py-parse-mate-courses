from dataclasses import dataclass, fields, astuple
import requests
from bs4 import BeautifulSoup, Tag
import csv

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course: Tag) -> Course:
    return Course(
        name=course.select_one("a.typography_landingH3__vTjok h3").text,
        short_description=course.select_one(
            "p.typography_landingTextMain__Rc8BD.mb-32"
        ).text.strip(),
        duration=course.select(".ProfessionCard_professionTags__2iarD.mb-24 span")[
            -1
        ].text,
    )


def get_all_courses() -> [Course]:
    response = requests.get(BASE_URL).content
    soup = BeautifulSoup(response, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__2Q8_V")
    return [parse_single_course(course) for course in courses]


def write_courses_to_file(courses: [Course]) -> None:
    with open("results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


if __name__ == "__main__":
    courses = get_all_courses()
    write_courses_to_file(courses)
