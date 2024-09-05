import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

MAIN_URL = "https://mate.academy"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_all_courses() -> list[Course]:
    main_page = requests.get(MAIN_URL)
    soup = BeautifulSoup(main_page.content, "html.parser")
    all_courses_soup = soup.select(".ProfessionCard_cardWrapper__JQBNJ")
    return [Course(
        name=course.select_one(
            ".typography_landingH3__vTjok.ProfessionCard_title__Zq5ZY.mb-12"
        ).text,
        short_description=course.select_one(
            ".typography_landingTextMain__Rc8BD.mb-32"
        ).text,
        duration=course.select_one(
            ".typography_landingTextMain__Rc8BD"
            ".ProfessionCard_subtitle__K1Yp6.mb-24"
        ).text
    )
        for course in all_courses_soup
    ]


def main() -> list[Course]:
    return get_all_courses()


if __name__ == "__main__":
    main()
