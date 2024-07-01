from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re
import csv

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    title: str
    description: str
    duration: int


def fetch_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def parse_single_course(course_soup: BeautifulSoup) -> Course:
    title_pattern = re.compile(r'ProfessionCard_title__[a-zA-Z0-9]{5}')
    subtitle_pattern = re.compile(r'ProfessionCard_subtitle__[a-zA-Z0-9]{5}')
    description_pattern = re.compile(r'typography_landingTextMain__[a-zA-Z0-9]{5}')

    title = course_soup.find(class_=title_pattern).get_text(strip=True)
    description = course_soup.find(class_=description_pattern).find_next('p').get_text(strip=True)

    subtitle = course_soup.find(class_=subtitle_pattern).get_text(strip=True)
    duration_match = re.search(r'\d+', subtitle)
    duration = int(duration_match.group()) if duration_match else 0

    return Course(
        title=title,
        description=description,
        duration=duration
    )


def get_all_courses(page_url: str) -> list[Course]:
    soup = fetch_html(page_url)
    card_wrappers = soup.find_all(class_=re.compile(r'ProfessionCard_cardWrapper__[a-zA-Z0-9]{5}'))

    courses = []
    for card_wrapper in card_wrappers:
        course = parse_single_course(card_wrapper)
        courses.append(course)

    return courses


def save_courses_to_csv(courses: list[Course], filename: str) -> None:
    print(f"Saving {len(courses)} courses to {filename}...")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Title", "Descriptions", "Durations"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for course in courses:
            writer.writerow({
                "Title": course.title,
                "Descriptions": course.description,
                "Durations": course.duration
            })
    print(f"Courses saved to {filename}.")


def main():
    courses = get_all_courses(BASE_URL)
    if courses:
        save_courses_to_csv(courses, "courses.csv")
    else:
        print("No courses found.")


if __name__ == "__main__":
    main()
