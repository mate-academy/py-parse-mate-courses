import aiohttp
import asyncio
import csv
from dataclasses import dataclass
from urllib.parse import urljoin
from typing import (
    List,
    Optional, Tuple
)
from bs4 import (
    BeautifulSoup,
    Tag
)


BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: int
    topics: int


async def fetch_page_content(
        url: str, session: aiohttp.ClientSession
) -> Optional[bytes]:
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()
    except aiohttp.ClientError:
        return None


async def fetch_course_details(
        url: str, session: aiohttp.ClientSession
) -> Tuple[int, int]:
    response = await fetch_page_content(urljoin(BASE_URL, url), session)
    soup = BeautifulSoup(response.decode("utf-8"), "html.parser")
    data = soup.select_one(
        "#course-program .CourseModulesHeading_headingGrid__ynoxV"
    )
    count_modules = count_topics = 0

    if data:
        count_modules = int(data.select_one(
            ".CourseModulesHeading_modulesNumber__UrnUh > p"
        ).text.split()[0])
        count_topics = int(data.select_one(
            ".CourseModulesHeading_topicsNumber__5IA8Z > p"
        ).text.split()[0])

    return count_modules, count_topics


async def crawl_course(
        tag: Tag, session: aiohttp.ClientSession
) -> Course:
    count_modules, count_topics = await fetch_course_details(
        tag.select_one("a.typography_landingH3__vTjok")["href"], session
    )
    return Course(
        name=tag.select_one(
            "a.typography_landingH3__vTjok > h3"
        ).get_text(),
        short_description=tag.select(
            "p.typography_landingTextMain__Rc8BD"
        )[1].get_text(),
        duration=tag.select(
            ".ProfessionCard_subtitle__K1Yp6 > span"
        )[0].get_text(),
        modules=count_modules,
        topics=count_topics
    )


async def async_get_all_courses() -> List[Course]:
    courses = []
    async with aiohttp.ClientSession() as session:
        response = await fetch_page_content(BASE_URL, session)
        soup = BeautifulSoup(response.decode("utf-8"), "html.parser")
        data = soup.select(
            "#all-courses .ProfessionCard_cardWrapper__JQBNJ"
        )

        if data:
            tasks = [
                crawl_course(course, session)
                for course in data
            ]
            courses = await asyncio.gather(*tasks)

    return courses


async def write_courses_to_csv(
        courses: List[Course], output_csv_path: str
) -> None:
    with open(
            output_csv_path, mode="w", newline="", encoding="utf-8"
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "name",
                "short_description",
                "duration",
                "topics",
                "modules"
            ]
        )

        for course in courses:
            writer.writerow(
                [
                    course.name,
                    course.short_description,
                    course.duration,
                    course.topics,
                    course.modules
                ]
            )


def get_all_courses() -> List[Course]:
    return asyncio.run(async_get_all_courses())


def main(output_csv_path: str) -> None:
    asyncio.run(write_courses_to_csv(get_all_courses(), output_csv_path))


if __name__ == "__main__":
    main("courses.csv")
