import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def parse_courses(course_elements: Tag) -> Course:
    name = course_elements.select_one("h3").text
    short_description = course_elements.select_one(
        "p.mb-32"
    ).text.strip()
    duration_elements = course_elements.select(
        "p[class*=ProfessionCardTags_regularTag]"
    )

    # Check if duration_elements is not empty before accessing its elements
    if duration_elements:
        if len(duration_elements) > 1:
            duration = duration_elements[1].text.strip()
        else:
            duration = duration_elements[0].text.strip()
    else:
        duration = "Duration not found"

    return Course(
        name=name,
        short_description=short_description,
        duration=duration,
    )


def get_all_courses(page_url: str = BASE_URL) -> List[Course]:
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    course_elements = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    courses = [
        parse_courses(
            course_element
        ) for course_element in course_elements
    ]
    return courses


if __name__ == "__main__":
    courses = get_all_courses(BASE_URL)
    for course in courses:
        print(course)
