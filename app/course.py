from dataclasses import dataclass
from enum import Enum


class CourseType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"


@dataclass
class Course:
    name: str
    short_description: str
    course_type: CourseType
    num_modules: int
    num_topics: int
    duration: str


# Course fields corresponding CSS selectors in Mate Academy
NAME = "a[class*=ProfessionCard_title]"
SHORT_DESCRIPTION = "p[class*='typography_landingTextMain__Rc8BD mb-32']"
PART_FULL_LINKS = ".ProfessionCard_buttons__a0o60 > a"
COURSE_TYPE = "head > meta[property='og:url']"
NUM_MODULES = "div.CourseModulesHeading_modulesNumber__UrnUh > p"
NUM_TOPICS = "div.CourseModulesHeading_topicsNumber__5IA8Z > p"
DURATION = "div.CourseModulesHeading_courseDuration__qu2Lx > p"

COURSES_CARD = "div[data-qa=profession-card]"
