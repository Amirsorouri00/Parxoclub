from django.utils import translation
from django.utils.translation import get_language, \
    get_supported_language_variant, ugettext_lazy as _
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone

import datetime
from .forkedcalendar import HTMLCalendar
from .models import Event
from Calendar import forkedcalendar
from Common.constants import CALENDAR_DAY_EVENTS, CALENDAR_DAY_OUT_OF_MONTH, \
    CALENDAR_DAY_WITHOUT_EVENTS, CALENDAR_DAY_WITH_EVENTS
from datetime import date, datetime as dtime, time


class EventCalendar(HTMLCalendar):
    language = None
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        print('in utils formatday: ' + str(day))
        print(self.language)
        today_day_number = forkedcalendar.PraxoCalendarVariables().today_day_num
        tmp = day
        tmp2 = 0
        if tmp == tmp2:
            return CALENDAR_DAY_OUT_OF_MONTH % ('disable')  # day outside month
        else:
            event_day = day
            if self.language == 'fa' or translation.get_language_bidi():
                date = JalaliDate(year = self.theyear, month = self.themonth, day = day).todate()
                event_day = date.day
            events_from_day = events.filter(day_of_the_event__day=event_day)
            
            print('final_events' + str(event_day))  
            print(events_from_day)
            if len(events_from_day) == 0:
                if day == today_day_number:
                    return CALENDAR_DAY_WITHOUT_EVENTS % ('active', day, event_day)
                else:    
                    return CALENDAR_DAY_WITHOUT_EVENTS % ('', day, event_day)
            else:
                events_html = "<ul>"
                for event in events_from_day:
                    events_html += event.get_absolute_url() + "<br>"
                events_html += "</ul>"
                if day == today_day_number:
                    return CALENDAR_DAY_WITH_EVENTS % ('active', day, day)
                else:
                    return CALENDAR_DAY_WITH_EVENTS % ('', day, day)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        if self.language == 'fa' or translation.get_language_bidi():
            s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        else: s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        self.language = get_supported_language_variant(get_language(), strict=False)
        
        
        v = []
        a = v.append
        a('<table class="amir_calendar_month">')
        a('\n')
        #a(self.formatmonthname(theyear, themonth, withyear=withyear))
        #a('\n')
        #a(self.formatweekheader())
        if self.language == 'fa' or translation.get_language_bidi():
            a('<thead> <tr> <th>شنبه</th> <th> یکشنبه</th> <th>دوشنبه</th> <th>سه شنبه</th> <th>چهارشنبه</th> <th>پنج شنبه</th> <th>جمعه</th> </tr> </thead>')
            #a('<thead> <tr> <th>جمعه</th> <th>پنج شنبه</th> <th>چهارشنبه</th> <th>سه شنبه</th> <th>دوشنبه</th> <th>یکشنبه</th> <th>شنبه</th> </tr> </thead>')
        else:
            a('<thead> <tr> <th>Mon</th> <th>Tue</th> <th>Wen</th> <th>Thu</th> <th>Fri</th> <th>Sat</th> <th>Son</th> </tr> </thead>')
        
        a('\n')
        self.theyear = theyear
        self.themonth = themonth
        #self.praxo_calendar_var = forkedcalendar.PraxoCalendarVariables()
        if self.language == 'fa' or translation.get_language_bidi():
            today = JalaliDate.today()
            self.julian = JalaliDate(year = theyear, month = themonth, day = today.day).todate()
        else: self.julian = datetime.date(year = theyear, month = themonth, day = 1)
        events = Event.objects.filter(day_of_the_event__month=self.julian.month)
        for week in self.monthdays2calendar(theyear, themonth): 
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
    def month_title(self, theyear, themonth, withyear=True):
        return self.formatmonthname(theyear, themonth, withyear=withyear)
    