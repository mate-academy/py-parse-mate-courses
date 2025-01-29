from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_courses(soup: BeautifulSoup) -> List[set]:
    names = soup.find_all(
        "h3",
        {"class": "ProfessionCard_title__m7uno typography_textH4__pLmyn"})
    short_descriptions = soup.find_all(
        "p",
        {"class": "c-text-platform-secondary typography_textMain__oRJ69 "
                  "ProfessionCard_text___l0Du ProfessionCard_description__K8weo"})
    durations = soup.find_all(
        "p",
        {"class": "c-text-platform-secondary typography_textMain__oRJ69 "
                  "ProfessionCard_text___l0Du ProfessionCard_duration__13PwX"})
    course_names = [name.text.strip() for name in names]
    course_descriptions = [desc.text.strip() for desc in short_descriptions]
    course_durations = [duration.text.strip() for duration in durations]

    course_data = zip(course_names, course_descriptions, course_durations)
    return course_data


def parse_courses(course_list: List[set]) -> List[Course]:
    return [Course(name=name,
                   short_description=description,
                   duration=duration)
            for name, description, duration in course_list]


def get_all_courses() -> List[Course]:
    base_url = "https://mate.academy"

    soup = fetch_page(base_url)
    courses = extract_courses(soup)
    return parse_courses(courses)


if __name__ == "__main__":
    get_all_courses()
