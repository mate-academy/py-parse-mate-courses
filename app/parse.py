import logging
import time
from dataclasses import dataclass
from functools import wraps
from typing import Any

from aiohttp import ClientSession, ClientTimeout
from bs4 import BeautifulSoup
import asyncio

BASE_URL = "https://mate.academy/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    module_count: int
    topics: list[tuple[str, str]]


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
    )


def log_time(func) -> Any:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        logging.info(
            f"Time taken by {func.__name__}: {time.time() - start_time:.2f} seconds"
        )
        return result

    return wrapper


async def get_page_content(session: ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=ClientTimeout(total=5)) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
    return ""


def parse_single_course(course: BeautifulSoup) -> Course:
    modules = course.select("div.CourseModulesList_moduleListItem__HKJqw")
    topics = [
        (
            module.select_one("p.CourseModulesList_topicName__ZrDxT").text,
            module.select_one(
                "p.CourseModulesList_topicsCount__yAPxH.typography_landingTextMain__Rc8BD"
            ).text,
        )
        for module in modules
    ]

    return Course(
        name=course.select_one("h1[data-qa='profession-title']").text.split(":")[0],
        short_description=course.select_one("p.typography_landingTextMain__Rc8BD").text,
        duration=course.select_one(
            ".ComparisonTable_tableBody__W5hzV.mb-24 > div:nth-of-type(7) > div:nth-of-type(2)"
        ).text,
        module_count=len(modules),
        topics=topics,
    )


async def get_courses_urls(session: ClientSession) -> list[str]:
    page_content = await get_page_content(session, BASE_URL)
    soup = BeautifulSoup(page_content, "html.parser")
    return list(
        set(
            course["href"].split("/courses/")[-1]
            for course in soup.select(
                ".HeaderCoursesDropdown_dropdownWrapper__3Agil a[href*='/courses/']"
            )
        )
    )


@log_time
async def get_all_courses() -> tuple[Any]:
    async with ClientSession() as session:
        course_urls = await get_courses_urls(session)
        tasks = [fetch_course(session, course) for course in course_urls]
        return await asyncio.gather(*tasks)


async def fetch_course(session: ClientSession, course_slug: str) -> Course | None:
    logging.debug(f"Fetching course: {course_slug}")
    course_page_content = await get_page_content(
        session, f"{BASE_URL}/courses/{course_slug}"
    )
    if course_page_content:
        soup = BeautifulSoup(course_page_content, "html.parser")
        return parse_single_course(soup)
    return None


if __name__ == "__main__":
    configure_logging()
    courses = asyncio.run(get_all_courses())

    seen_courses = set()
    for course in courses:
        if course and course.name not in seen_courses:
            seen_courses.add(course.name)
            print(
                f"Name: {course.name}\nDescription: {course.short_description}\nDuration: {course.duration}\n"
                f"Module Count: {course.module_count}\nModules:"
            )
            for topic, count in course.topics:
                print(f"  - {topic}: {count}")
            print()
