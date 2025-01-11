import logging
import sys
import time
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


BASE_URL = "https://mate.academy/"


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)8s]: %(message)s",
    handlers=[
        logging.FileHandler("parser.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    topics_count: int
    modules_count: int


def get_page_content() -> BeautifulSoup:
    """Get and parse HTML content from mate.academy website."""
    logging.info("Fetching main page content...")
    response = requests.get(BASE_URL)
    return BeautifulSoup(response.content, "html.parser")


def get_course_details(course_url: str) -> tuple[int, int]:
    """Get detailed information about course from its page."""
    logging.info(f"Processing course page: {course_url}")
    driver = webdriver.Chrome()

    try:
        driver.get(course_url)

        # Get topics count from fact block
        topics_elements = driver.find_elements(
            By.CSS_SELECTOR, "p[class*='FactBlock_factNumber__']"
        )
        topics_count = int(
            next(
                element.text.strip()
                for element in topics_elements
                if element.text.strip()
                and element.text.strip()[0].isdigit()
                and "%" not in element.text
            )
        )
        logging.info(f"Found {topics_count} topics")

        # Find "Show more" button
        show_more_button = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "button[class*='CourseModulesList_showMore__']",
                )
            )
        )

        # Click using JavaScript
        driver.execute_script("arguments[0].click();", show_more_button)
        time.sleep(1)

        # Count modules
        modules = driver.find_elements(
            By.CSS_SELECTOR, "div[class*='CourseModulesList_moduleListItem__']"
        )
        modules_count = len(modules)
        logging.info(f"Found {modules_count} modules")

        return topics_count, modules_count

    finally:
        driver.quit()


def parse_course(card: Tag) -> Course:
    """Extract course information from a course card."""
    name = card.select_one("h3").text.strip()
    logging.info(f"Processing course: {name}")
    short_description = card.select_one(
        "p[class*='typography_landingTextMain__Rc8BD mb-32']"
    ).text.strip()

    tags = card.select("p[class*='ProfessionCardTags_regularTag__']")
    duration = next(
        tag.text.strip() for tag in tags if tag.text.strip()[0].isdigit()
    )

    # Get course URL and fetch additional details
    course_url = BASE_URL.rstrip("/") + card.select_one("a")["href"]
    topics_count, modules_count = get_course_details(course_url)

    return Course(
        name, short_description, duration, topics_count, modules_count
    )


def get_all_courses() -> list[Course]:
    """Get list of all courses from mate.academy website."""
    logging.info("Starting courses parsing...")
    page_content = get_page_content()
    course_cards = page_content.select(
        "div[class*='ProfessionCard_cardWrapper__']"
    )
    logging.info(f"Found {len(course_cards)} courses to process")

    courses = [parse_course(card) for card in course_cards]
    logging.info("Finished parsing all courses")

    return courses


if __name__ == "__main__":
    courses = get_all_courses()
    print(f"\nTotal courses parsed: {len(courses)}")
