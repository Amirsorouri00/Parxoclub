from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event
from Common.constants import CALENDAR_DAY_WITHOUT_EVENTS, CALENDAR_DAY_WITH_EVENTS, CALENDAR_DAY_EVENTS, CALENDAR_DAY_OUT_OF_MONTH


class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return CALENDAR_DAY_OUT_OF_MONTH % ('disable')  # day outside month
        else:
            events_from_day = events.filter(day_of_the_event__day=day)
            if len(events_from_day) == 0:
                return CALENDAR_DAY_WITHOUT_EVENTS % ('', day, day)
            else:
                events_html = "<ul>"
                for event in events_from_day:
                    events_html += event.get_absolute_url() + "<br>"
                events_html += "</ul>"
                return CALENDAR_DAY_WITH_EVENTS % ('', day, day)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        events = Event.objects.filter(day_of_the_event__month=themonth)
        v = []
        a = v.append
        a('<table class="amir_calendar_month">')
        a('\n')
        #a(self.formatmonthname(theyear, themonth, withyear=withyear))
        #a('\n')
        #a(self.formatweekheader())
        a('<thead> <tr> <th>Son</th> <th>Mon</th> <th>Tue</th> <th>Wen</th> <th>Thu</th> <th>Fri</th> <th>Sat</th> </tr> </thead>')
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)