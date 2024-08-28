import asyncio
import json
from dataclasses import dataclass, asdict

import bs4
import httpx
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    count_modules: int
    count_topics: int


async def get_detail_course(url: str, client: httpx.AsyncClient) -> dict[str, int]:
    response = await client.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.text, "html.parser")
    data_container = soup.select_one("#course-program .CourseModulesHeading_headingGrid__ynoxV")
    return {
        "count_modules": int(data_container.select_one(
            ".CourseModulesHeading_modulesNumber__UrnUh > p"
        ).text.split(" ")[0]),
        "count_topics": int(data_container.select_one(
            ".CourseModulesHeading_topicsNumber__5IA8Z > p"
        ).text.split(" ")[0]),
    }


async def parse_course(tag: bs4.Tag, client: httpx.AsyncClient) -> Course:
    extra_data = await get_detail_course(
        tag.select_one("a.typography_landingH3__vTjok")["href"], client
    )
    return Course(
        name=tag.select_one("a.typography_landingH3__vTjok > h3").text,
        short_description=tag.select("p.typography_landingTextMain__Rc8BD")[1].text,
        duration=tag.select(".ProfessionCard_subtitle__K1Yp6 > span")[0].text,
        count_modules=extra_data["count_modules"],
        count_topics=extra_data["count_topics"],
    )


async def get_all_courses() -> list[Course]:
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    courses = soup.select("#all-courses .ProfessionCard_cardWrapper__JQBNJ")

    client = httpx.AsyncClient()
    results = list(await asyncio.gather(*[
        parse_course(course, client)
        for course in courses
    ]))
    await client.aclose()
    return results


def write_courses_json(courses: list[Course], file_name: str) -> None:
    with open(file_name, "w", encoding="utf-8") as f:
        data = json.dumps([asdict(course) for course in courses], indent=4, ensure_ascii=False)
        f.write(data)


async def main():
    write_courses_json(await get_all_courses(), "data.json")


if __name__ == "__main__":
    asyncio.run(main())
