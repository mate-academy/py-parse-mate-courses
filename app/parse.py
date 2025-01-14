import requests
import csv
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass, fields, astuple


BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


COURSE_FIELDS = [field.name for field in fields(Course)]


def parse_single_course(course: Tag) -> Course:
    name = course.select_one("a.typography_landingH3__vTjok h3")
    short_description = (
        course.select_one("p.typography_landingTextMain__Rc8BD.mb-32"))
    duration_tags = (course.select(
        ".ProfessionCard_professionTags__2iarD.mb-24 span")
    )

    if not all([name, short_description, duration_tags]):
        raise ValueError("Missing required course data")

    last_duration = duration_tags[-1].text.strip() if duration_tags else ""

    return Course(
        name=name.text.strip(),
        short_description=short_description.text.strip(),
        duration=last_duration
    )


def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    course_elements = soup.select("div.ProfessionCard_cardWrapper__2Q8_V")
    courses = []

    for element in course_elements:
        try:
            course = parse_single_course(element)
            courses.append(course)
        except AttributeError:
            continue

    return courses


def write_courses_to_csv(courses: [Course], path: str) -> None:
    """Save courses to CSV file"""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COURSE_FIELDS)
        writer.writerows([astuple(course) for course in courses])


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    write_courses_to_csv(courses, output_csv_path)


if __name__ == "__main__":
    main("courses.csv")
