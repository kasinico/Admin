document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth'
    });
  
    calendar.render();
  });

  
  $(document).ready(function() {
    // page is now ready, initialize the calendar...
    $('#calendar').fullCalendar({
        // put your options and callbacks here
        // for example:
        defaultView: 'month',
        events: [
            {
                title  : 'event1',
                start  : '2018-01-01'
            },
            {
                title  : 'event2',
                start  : '2018-01-05',
                end    : '2018-01-07'
            },
            {
                title  : 'event3',
                start  : '2018-01-09T12:30:00',
                allDay : false // will make the time show
            }
            // other events here...
        ]
    });
});
