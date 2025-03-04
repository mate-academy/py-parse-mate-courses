import csv
import sys
import logging
from dataclasses import astuple, dataclass, fields

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://mate.academy/"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("parser.log"),
        logging.StreamHandler(sys.stdout)
    ],
)


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules_number: int
    topics_number: int


COURSE_FIELDS = [field.name for field in fields(Course)]


def get_courses_links(main_page_soup: BeautifulSoup) -> dict[str, str]:
    courses = main_page_soup.select(".DropdownProfessionsItem_item__BRxO2")
    links = {}
    for course in courses:
        course_link = course.select_one("a[href*='/courses']")["href"]
        course_name = course.select_one("a[href*='/courses']").get_text()
        links[course_link] = course_name
    return links


def parse_single_course(course_link: str, course_name: str) -> Course:
    try:
        text = requests.get(BASE_URL + course_link, timeout=5).content
        main_page_soup = BeautifulSoup(text, "html.parser")
        name = course_name
        short_description = main_page_soup.select_one(
            ".SalarySection_aboutProfession__1VFHK"
        ).get_text()

        duration = ""
        rows = main_page_soup.select(".ComparisonTable_row__q3PSK")
        for row in rows:
            cells = row.select(".ComparisonTable_cell__RNsyU")
            if len(cells) == 2 and cells[0].get_text().strip() == "Тривалість":
                duration = cells[1].get_text().strip()
                break

        mod_num = len(
            main_page_soup.select(".CourseModulesList_topicName__ZrDxT")
        )
        topic_num = (
            main_page_soup.
            select_one(".FactBlock_factNumber__d_8nn").get_text()
        )

        return Course(name, short_description, duration, mod_num, topic_num)
    except Exception as e:
        logging.error(f"Error parsing course {course_name}: {e}")
        return Course(course_name, "", "", 0, 0)


def get_all_courses() -> list[Course]:
    try:
        logging.info("Getting courses...")
        text = requests.get(BASE_URL, timeout=5).content
        main_page_soup = BeautifulSoup(text, "html.parser")
        courses_links = get_courses_links(main_page_soup)
        courses_list = []
        for course_link, course_name in courses_links.items():
            logging.info(f"Got course: {course_name}")
            courses_list.append(parse_single_course(course_link, course_name))

        return courses_list
    except Exception as e:
        logging.error(f"Error getting courses: {e}")
        return []


def write_courses_to_csv(courses: list[Course], output_csv_path: str) -> None:
    try:
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(COURSE_FIELDS)
            writer.writerows(astuple(course) for course in courses)
    except Exception as e:
        logging.error(f"Error writing courses to CSV: {e}")


if __name__ == "__main__":
    write_courses_to_csv(get_all_courses(), "courses.csv")
