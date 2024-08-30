import asyncio
import time
from dataclasses import dataclass
from typing import Optional

import httpx
import requests
from bs4 import BeautifulSoup


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    count_modules: Optional[int] = None
    count_topics: Optional[int] = None


async def get_aditional_info(url: str, course_elem: Course) -> None:
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        response = await client.get("https://mate.academy" + url)
        print(f"answer {url} was got {time.time() - start_time: .2f} sec")
        soup = BeautifulSoup(response.text, "html.parser")
        data_container = soup.select_one(
            "#course-program .CourseModulesHeading_headingGrid__ynoxV"
        )
        if data_container:
            modules_elem = data_container.select_one(
                ".CourseModulesHeading_modulesNumber__UrnUh > p"
            )
            if modules_elem:
                course_elem.count_modules = int(
                    modules_elem.text.split(" ")[0]
                )
            topics_elem = data_container.select_one(
                ".CourseModulesHeading_topicsNumber__5IA8Z > p"
            )
            if topics_elem:
                course_elem.count_topics = int(topics_elem.text.split(" ")[0])


async def fetch_all_courses() -> list[Course]:
    page = requests.get("https://mate.academy").content
    soup = BeautifulSoup(page, "html.parser")
    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    course_list = []
    tasks = []

    for course in courses:
        course_name_elem = course.find("h3")
        course_name = course_name_elem.get_text()\
            if course_name_elem else "No Name"

        course_duration_elem = course.select_one(
            "[class^='typography_landingTextMain'] > span"
        )
        course_duration = course_duration_elem.get_text() \
            if course_duration_elem else "No Duration"

        description_elem = course.find(
            "p",
            class_="typography_landingTextMain__Rc8BD mb-32"
        )
        description = description_elem.get_text() \
            if description_elem else "No Description"

        course_elem = Course(
            name=course_name,
            short_description=description,
            duration=course_duration
        )

        url_element = course.select_one("a.typography_landingH3__vTjok")
        if url_element:
            url = url_element["href"]
            tasks.append(get_aditional_info(url, course_elem))
        else:
            print("No URL found for course")

        course_list.append(course_elem)

    await asyncio.gather(*tasks)

    return course_list


def get_all_courses() -> list[Course]:
    return asyncio.run(fetch_all_courses())


if __name__ == "__main__":
    courses = get_all_courses()
    for course in courses:
        print(course)
