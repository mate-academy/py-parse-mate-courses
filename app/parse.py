import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


BASE_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str
    modules: str
    topics: str


def get_one_course(courses_soup: BeautifulSoup) -> Course:
    modules_and_topics_href = courses_soup.select_one(
        ".typography_landingH3__vTjok"
    )["href"]
    page_with_modules_and_topics_info = requests.get(
        BASE_URL + modules_and_topics_href
    ).content
    soup = BeautifulSoup(
        page_with_modules_and_topics_info,
        "html.parser",
    )

    modules_class = ".CourseModulesHeading_modulesNumber__UrnUh"
    topics_class = ".CourseModulesHeading_topicsNumber__5IA8Z"

    return Course(
        name=courses_soup.select_one("h3").text,
        short_description=courses_soup.select_one(".mb-32").text,
        duration=courses_soup.select_one(".mb-24 > span").text,
        modules=soup.select_one(modules_class).text,
        topics=soup.select_one(topics_class).text,
    )


def get_all_courses() -> list[Course]:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    courses = soup.select(".ProfessionCard_cardWrapper__JQBNJ")

    return [get_one_course(courses_soup) for courses_soup in courses]


if __name__ == "__main__":
    print(get_all_courses())
