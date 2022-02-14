var newEvent;
var editEvent;

$(document).ready(function() {

   var calendar = $('#calendar').fullCalendar({

       eventRender: function(event, element, view) {

           var show_calendar = true;


           var calendars = $('#calendar_filter').val();

           if (calendars && calendars.length > 0) {
               if (calendars[0] == "all") {
                   show_calendar = true;
               } else {
                   show_calendar = calendars.indexOf(event.calendar) >= 0;
               }
           }

           return show_username && show_type && show_calendar;

       },



       defaultDate: moment('2018-03-07'),


   });

   $('.filter').on('change', function() {
       $('#calendar').fullCalendar('rerenderEvents');
   });

   $("#type_filter").select2({
       placeholder: "Filter Types",
       allowClear: true
   });

   $("#calendar_filter").select2({
       placeholder: "Filter Calendars",
       allowClear: true
   });

});



