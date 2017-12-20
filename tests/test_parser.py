from datetime import date
from spb_dnevnik_bot import parser


class TestDay:
    def test_add_lesson(self):
        the_date = date.today()
        day = parser.Day(the_date)
        assert len(day.lessons) == 0, "Shouldn't be any lessons"
        day.add_lesson(parser.Lesson(1, 1, 'Some lesson', 'Some descr', None, None))
        assert len(day.lessons) == 1, "Should increase lessons"
