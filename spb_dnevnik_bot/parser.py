import logging
import os
from datetime import date, timedelta
from operator import methodcaller
from typing import Optional, NamedTuple, Tuple, List

import dateparser
from lxml.html import fromstring
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)
logging.getLogger('selenium').propagate = False

basedir = os.path.dirname(__file__)
phantomjs_executable = os.path.join(basedir, 'lib', 'phantomjs')


class Lesson(NamedTuple):
    id: int
    number: int
    name: str
    description: str
    mark: Optional[int]
    homework: Optional[str]


class Day:
    def __init__(self, the_date: date) -> None:
        self.date = the_date
        self.lessons: List[Lesson] = []

    def add_lesson(self, lesson: Lesson) -> None:
        self.lessons.append(lesson)


DAYS_TABLE_CLASS = 'week-lessons'


class LoginSession:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.base_url = 'https://petersburgedu.ru/dnevnik'
        self.timetable_url = f'{self.base_url}/timetable'

    def login(self) -> None:
        raise NotImplemented

    def get_timetable_page(self, dairy_date: date) -> str:
        """Get time table page text"""
        raise NotImplemented


class EsiaSession(LoginSession):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        self.driver = webdriver.PhantomJS(phantomjs_executable)
        self.driver.set_window_size(1120, 550)  # there was some bug in driver
        self.login_url = 'https://petersburgedu.ru/user/auth/login'

    def login(self) -> None:
        """Trying to login with esia"""
        self.driver.get(self.login_url)
        e = self.driver.find_element_by_class_name('esia-login')
        e.click()
        username = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.ID, 'mobileOrEmail'))
        )
        logger.debug("Got login page %s", self.driver.current_url)
        username.send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        e = self.driver.find_element_by_xpath('//div[@class="line-btns"]/button')
        e.click()

    def get_timetable_page(self, dairy_date: date) -> str:
        """Get time table page text"""
        self.driver.get(f'{self.base_url}/timetable?date={dairy_date:%d.%m.%Y}')
        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, DAYS_TABLE_CLASS))
        )
        logger.debug("Got timetable page at %s", self.driver.current_url)
        return self.driver.page_source


class Parser:
    def __init__(self, username: str, password: str, diary_date: date = None) -> None:
        logger.info("Starting to parse with %s/%s", username, password)
        self.session = EsiaSession(username, password)
        self.diary_date = diary_date or date.today()

    def login(self) -> None:
        self.session.login()

    def get_timetable(self) -> List[Day]:
        """Get timetable page object as list of Day"""
        page_xml = fromstring(self.session.get_timetable_page(self.diary_date))
        days_table = page_xml.xpath(f'//table[@class="{DAYS_TABLE_CLASS}"]')[0]
        days_count = len(days_table.xpath('thead/tr/th'))
        logger.debug("Days on timetable %s", days_count)
        begin_date, end_date = self.get_date_range(page_xml)
        logger.debug("Days on timetable from %s till %s", begin_date, end_date)
        days = []
        for day_number in range(1, days_count + 1):
            # We only want lesson itself. Don't need time and number
            cell_xpath = f'tbody/tr[not (contains(@class, "lesson-about"))]/td[{day_number}]'
            current_date = begin_date + timedelta(days=day_number - 1)
            day = Day(current_date)
            for idx, cell in enumerate(days_table.xpath(cell_xpath), 1):
                try:
                    lesson_id = cell.xpath('h5/a/@href')[0]
                except IndexError:
                    lesson_id = None
                else:
                    lesson_id = lesson_id.rpartition('/')[-1]
                name = self.xpath_text(cell, 'h5/a')
                description = self.xpath_text(cell, 'p[@class="about"]')
                homework = self.xpath_text(cell, 'p[@class="homework"]')
                grade = self.xpath_text(cell, 'span[@class="grade"]')
                lesson = Lesson(lesson_id, idx, name, description, grade, homework)
                day.add_lesson(lesson)
            days.append(day)
        return days

    @staticmethod
    def xpath_text(xelement, xpath: str) -> Optional[str]:
        text = xelement.xpath(f"{xpath}/text()")
        result = ', '.join(filter(bool, map(methodcaller('strip'), text)))
        result = result.replace('\n', ', ')
        return result or None

    def get_date_range(self, page) -> Tuple[date, date]:
        range_str = page.xpath('id("period")/div[1]/div[@class="title"]/text()')[0]
        begin, end = [dateparser.parse(s) for s in range_str.split('-')]
        return begin.date(), end.date()

    def get_diary(self) -> List[Lesson]:
        logger.debug("User needs %s", self.diary_date)
        day = next(day for day in self.get_timetable() if day.date == self.diary_date)
        return day.lessons
