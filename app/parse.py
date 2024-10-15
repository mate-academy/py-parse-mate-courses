import csv
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from dataclasses import dataclass, fields
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


class Driver:
    instance = None

    @staticmethod
    def initialize() -> webdriver.Chrome:
        if Driver.instance is None:
            Driver.instance = webdriver.Chrome()
        return Driver.instance


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    num_topics: str | None = None
    num_modules: str | None = None


def parse_single_course(soup: BeautifulSoup) -> Course:
    name = soup.select_one(".ProfessionCard_title__Zq5ZY").text
    short_description = soup.select_one(
        ".ProfessionCard_cardWrapper__JQBNJ >"
        " p.typography_landingTextMain__Rc8BD"
    ).text
    duration = soup.select(
        ".ProfessionCard_professionTags__kCD1H > "
        "p.ProfessionCardTags_regularTag__yTc6K"
    )[-1].text

    course = Course(
        name=name,
        short_description=short_description,
        duration=duration
    )
    return course


def add_num_topics_and_num_modules(
        soup: BeautifulSoup,
        course: Course
) -> Course:
    details = soup.select_one(".typography_landingH3__vTjok")["href"]
    course_details_url = BASE_URL + details

    num_topics = parse_num_topics(course_details_url)
    num_modules = parse_num_modules(course_details_url)

    course.num_topics = num_topics
    course.num_modules = num_modules
    return course


def parse_num_topics(page_url: str) -> str:
    page = requests.get(page_url).content
    soup = BeautifulSoup(page, "html.parser")

    num_topics = soup.select_one(
        ".CourseProgram_purple__STsuM > .FactBlock_factNumber__d_8nn"
    ).text

    return num_topics


def parse_num_modules(page_url: str) -> str:
    driver = Driver.initialize()
    driver.get(page_url)
    find_button = driver.find_element(
        By.CLASS_NAME,
        "CourseProgram_modules__GA_PJ"
    )
    button_more = find_button.find_element(
        By.CLASS_NAME,
        "Button_neutral__ueX17"
    )
    to_scroll = driver.find_element(
        By.CLASS_NAME,
        "CourseProgram_modules__GA_PJ"
    )
    driver.execute_script("arguments[0].scrollIntoView();", to_scroll)

    time.sleep(5)
    button_more.click()

    updated_page = driver.page_source
    updated_soup = BeautifulSoup(updated_page, "html.parser")

    num_modules = updated_soup.select(
        ".CourseProgram_modules__GA_PJ > ul > li.color-dark-blue > "
        ".CourseModulesList_moduleListItem__HKJqw > "
        ".CourseModulesList_itemLeft__HP6K3 > "
        "p.CourseModulesList_topicName__ZrDxT"
    )

    return str(len(num_modules))


def get_all_courses() -> [Course]:
    page = requests.get(BASE_URL + "/en/").content
    soup = BeautifulSoup(page, "html.parser")

    courses_info = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    courses = []
    for course_soup in courses_info:
        course = parse_single_course(course_soup)
        add_info = add_num_topics_and_num_modules(course_soup, course)
        courses.append(add_info)
    return courses


def write_courses(output_csv_path: str, courses: list[Course]) -> None:
    with open(output_csv_path, "w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerow([field.name for field in fields(Course)])
        for course in courses:
            writer.writerow(
                [
                    course.name,
                    course.short_description,
                    course.duration,
                    course.num_topics,
                    course.num_modules
                ]
            )


def main(output_csv_path: str) -> None:
    courses = get_all_courses()
    write_courses(output_csv_path, courses)


if __name__ == "__main__":
    main("courses.csv")
