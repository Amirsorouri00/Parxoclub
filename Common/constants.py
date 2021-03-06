from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


import datetime
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone
from django.utils import translation
from django.utils.translation import get_language, \
    get_supported_language_variant, ugettext_lazy as _

class PraxoCalendarFunctions():
    # language = ''
    # mydate, mydatetime, January, February, mdays = [1,1,1,1,1]
    
    def __init__(self):
        # language = self.SetLanguage()
        # mydate, mydatetime, January, February, mdays = self.SetVars(self)
        self.language = self.SetLanguage()
        self.mydate, self.mydatetime, self.January, self.February, self.mdays = self.SetVars()
    
    def SetLanguage(self):
        language = get_supported_language_variant(get_language(), strict=False)
        return language

    def SetVars(self):
        language = self.SetLanguage()
        if language == 'fa' or translation.get_language_bidi():
            mydate = JalaliDate
            mydatetime = JalaliDatetime
            January = 1
            February = 12
            mdays = [0, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
            return mydate, mydatetime, January, February, mdays
        else: 
            mydate = datetime.date
            mydatetime = datetime.datetime
            January = 1
            February = 2
            mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return mydate, mydatetime, January, February, mdays

# class PraxoCalendarVariables(PraxoCalendarFunctions):
#     language = SetLanguage()
#     mydate, mydatetime, January, February, mdays = SetVars()


LORE_IPSUM = 'Lorem ipsum dolor sit amet, ad viris mediocrem vis. Essent referrentur quo id, blandit recusabo in eos, mundi albucius ad duo. Sale utroque singulis pro at, mea affert dicunt no. Equidem hendrerit mediocritatem id vel, iudico alienum deserunt mea id. At eum eirmod vivendum.'


CHAT_CONSUMER_PREFIX_GROUP_NAME = 'chat_%s'
USER_STRING = 'USER-PRIVATE-KEY'
ROOM_STRING = 'ROOM-PRIVATE-KEY'
USER_CONTACT_HAVE_ROOM = 'UserHaveRoomWithContact'
USER_EXIST_IN_ROOM = 'UserExistInTheRoom'
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
CHOICES = (
    (1, 'Gold'),
    (2, 'Bronz'),
    (3, 'Silver'),
    (4, 'Normal')
)

EVENT_TYPE_COLOR_CHOICES = (
    ('RED', 'RED'),
    ('YELLOW', 'GREEN'),
    ('GREEN', 'GREEN'),
    ('BLUE', 'BLUE')
)

CALENDAR_TABLE = "<table> <thead> <tr> <th>Son</th> <th>Mon</th> <th>Tue</th> <th>Wen</th> <th>Thu</th> <th>Fri</th> <th>Sat</th> </tr> </thead> <tbody> <tr> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>29</span> <span class='date-2'>29</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>30</span> <span class='date-2'>30</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>31</span> <span class='date-2'>31</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>1</span> <span class='date-2'>1</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>2</span> <span class='date-2'>2</span> </div> </div> </td> <td class='active'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>3</span> <span class='date-2'>3</span> </div> <div class='event-cell-container'> <div class='event-badge bg-yellow'> <span class='event-count'>6</span> <span class='event-type'>Operation</span> </div> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>4</span> <span class='date-2'>4</span> </div> </div> </td> </tr> <tr> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>5</span> <span class='date-2'>5</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>6</span> <span class='date-2'>6</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>7</span> <span class='date-2'>7</span> </div> </div> </td> <td class='today'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>8</span> <span class='date-2'>8</span> </div> <div class='event-cell-container'> <div class='event-badge bg-blue'> <span class='event-count'>15</span> <span class='event-type'>Clinic </span> </div> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>9</span> <span class='date-2'>9</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>10</span> <span class='date-2'>10</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>11</span> <span class='date-2'>11</span> </div> </div> </td> </tr> <tr> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>12</span> <span class='date-2'>12</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>13</span> <span class='date-2'>13</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>14</span> <span class='date-2'>14</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>15</span> <span class='date-2'>15</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>16</span> <span class='date-2'>16</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>17</span> <span class='date-2'>17</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>18</span> <span class='date-2'>18</span> </div> </div> </td> </tr> <tr> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>19</span> <span class='date-2'>19</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>20</span> <span class='date-2'>20</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>21</span> <span class='date-2'>21</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>22</span> <span class='date-2'>22</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>23</span> <span class='date-2'>23</span> </div> <div class='event-cell-container'> <div class='event-badge bg-red'> <span class='event-count'>24</span> <span class='event-type'>Pharmacy </span> </div> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>24</span> <span class='date-2'>24</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>25</span> <span class='date-2'>25</span> </div> </div> </td> </tr> <tr> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>26</span> <span class='date-2'>26</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>27</span> <span class='date-2'>27</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>28</span> <span class='date-2'>28</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>29</span> <span class='date-2'>29</span> </div> </div> </td> <td class=''> <div class='date-cell'> <div class='date-container'> <span class='date-1'>30</span> <span class='date-2'>30</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>1</span> <span class='date-2'>1</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>2</span> <span class='date-2'>2</span> </div> </div> </td> </tr> <tr> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>3</span> <span class='date-2'>3</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>4</span> <span class='date-2'>4</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>5</span> <span class='date-2'>5</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>6</span> <span class='date-2'>6</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>7</span> <span class='date-2'>7</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>8</span> <span class='date-2'>8</span> </div> </div> </td> <td class='disable'> <div class='date-cell'> <div class='date-container'> <span class='date-1'>9</span> <span class='date-2'>9</span> </div> </div> </td> </tr> </tbody> </table>" 
CALENDAR_DAY_WITH_EVENTS = '<td class="%s"> <div class="date-cell"> <div class="date-container"> <span class="date-1">%d</span> <span class="date-2">%d</span> </div> <div class="event-cell-container"> <div class="event-badge bg-blue"> <span class="event-count">15</span> <span class="event-type">Clinic </span> </div> </div> </div> </td>'
CALENDAR_DAY_EVENTS = '<div class="event-cell-container"> <div class="event-badge bg-blue"> <span class="event-count">15</span> <span class="event-type">Clinic </span> </div> </div>'
CALENDAR_DAY_WITHOUT_EVENTS = '<td class="%s"> <div class="date-cell"> <div class="date-container"> <span class="date-1">%d</span> <span class="date-2">%d</span> </div> </div> </td>'
CALENDAR_DAY_OUT_OF_MONTH = '<td class="%s"> <div class="date-cell"> <div class="date-container"> <span class="date-1"></span> <span class="date-2"></span> </div> </div> </td>'