import asyncio
import logging
import sys
import time
from dataclasses import dataclass

import aiohttp
import selenium.common.exceptions
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


BASE_URL = "https://mate.academy/"
MAX_CONCURRENT_REQUESTS = 2


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


async def get_page_content() -> BeautifulSoup:
    """Get and parse HTML content from mate.academy website."""
    logging.info("Fetching main page content...")
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as response:
            html = await response.text()
            return BeautifulSoup(html, "html.parser")


async def get_course_details(
    course_url: str,
    semaphore: asyncio.Semaphore,
    driver_pool: list[webdriver.Chrome],
) -> tuple[int, int]:
    """Get detailed information about course from its page."""
    logging.info(f"Processing course page: {course_url}")

    async with semaphore:
        while not driver_pool:
            await asyncio.sleep(1)
            logging.warning("Waiting for available driver...")

        # Get available driver from pool
        driver = driver_pool.pop()

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

            show_more_button = WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (
                        By.TAG_NAME,
                        "button",
                    )
                )
            )

            show_more_button.click()
            await asyncio.sleep(1)

            modules = driver.find_elements(
                By.CSS_SELECTOR,
                "div[class*='CourseModulesList_moduleListItem__']",
            )
            modules_count = len(modules)

            return topics_count, modules_count

        except (
            selenium.common.exceptions.TimeoutException,
            selenium.common.exceptions.WebDriverException,
        ) as error:
            logging.error(f"Error processing {course_url}: {str(error)}")
            raise

        finally:
            # Return driver to pool
            driver_pool.append(driver)


async def parse_course(
    card: Tag,
    semaphore: asyncio.Semaphore,
    driver_pool: list[webdriver.Chrome],
) -> Course:
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
    topics_count, modules_count = await get_course_details(
        course_url, semaphore, driver_pool
    )

    return Course(
        name, short_description, duration, topics_count, modules_count
    )


async def get_all_courses() -> list[Course]:
    """Get list of all courses from mate.academy website."""
    logging.info("Starting courses parsing...")
    page_content = await get_page_content()
    course_cards = page_content.select(
        "div[class*='ProfessionCard_cardWrapper__']"
    )
    logging.info(f"Found {len(course_cards)} courses to process")

    driver_pool = []

    try:
        for _ in range(MAX_CONCURRENT_REQUESTS):
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")

                driver = webdriver.Chrome(options=chrome_options)
                driver_pool.append(driver)

            except selenium.common.exceptions.WebDriverException as error:
                logging.error(f"Error creating Chrome driver: {str(error)}")

                if not driver_pool:
                    raise
                break

        if not driver_pool:
            raise RuntimeError("Failed to create any Chrome driver")

        logging.info(f"Created {len(driver_pool)} Chrome drivers")
        semaphore = asyncio.Semaphore(len(driver_pool))

        courses = await asyncio.gather(
            *(
                parse_course(card, semaphore, driver_pool)
                for card in course_cards
            )
        )
        logging.info("Finished parsing all courses")
        return courses

    finally:
        for driver in driver_pool:
            try:
                driver.quit()

            except selenium.common.exceptions.WebDriverException as error:
                logging.error(f"Error closing Chrome driver: {str(error)}")


if __name__ == "__main__":
    start_time = time.time()
    courses = asyncio.run(get_all_courses())
    print(courses)
    end_time = time.time()

    print(f"\nTotal courses parsed: {len(courses)}")
    print(f"Time taken: {end_time - start_time} seconds")
