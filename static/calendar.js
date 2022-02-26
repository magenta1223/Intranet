// calendar
document.addEventListener('DOMContentLoaded', function() {

    let currentDayDate = new Date().toISOString().slice(0, 10);
    let checkbox = document.getElementsByClassName('badgebox');

    let calendarEl = document.getElementById('calendar');

    let calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap',
        height: '700px',
        expandRows: true,
        slotMinTime: '08:00',
        slotMaxTime: '20:00',
        headerToolbar: {
          left: 'title prev next',
          right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },


        buttonText: {
          today:    '오늘',
          month:    '월',
          week:     '주',
          day:      '일',
          list:     '목록'
        },


        initialView: 'dayGridMonth',
        navLinks: true,
        editable: false,
        selectable: true,
        nowIndicator: true,
        dayMaxEvents: 5,
        locale: 'ko',

        eventDidMount: function(info) { // display가 되는 event만 넘어옴. 즉, 꺼주어야 한다.

            let count = 0;
            let box_count = 0;

            for (var i = 0; i < checkbox.length; i++) {
                if (checkbox[i].checked == true) {
                    box_count ++ ;
                    if (!(checkbox[i].value == info.event.backgroundColor || checkbox[i].value == "all")) {
                        count ++ ;
                        };
                    };
                };

            if (count == box_count) {
                info.el.style.display = 'none';
                };

            var users = info.event.extendedProps.users;
            var description = info.event.extendedProps.description;
            var start = moment(info.event.start).format('YYYY/MM/DD');
            var end = moment(info.event.end).subtract(1, 'minutes').format('YYYY/MM/DD');
            var content = '';

            content = content + '<div class = "ct" style="border-top-color:'+info.event.backgroundColor+'!important" >'
            content = content + '<div class = "ct-content" style = "font-size:16px;margin-top:10px;">' + info.event.title + '</div>'
            content = content + '<div class = "ct-content" style = "font-size:12px;">' + start + ' ~ ' + end + ' </div><br>';
            content = content + '<div class = "ct-content" style = "font-size:14px;"> <i class="fa-solid fa-user"></i>&nbsp;&nbsp; ' + users + '</div>';
            
            if (info.event.extendedProps.type.includes('휴가')){
                content = content + '<div class = "ct-content" style = "font-size:14px;">' + info.event.extendedProps.type + '</div>'

            } else {
                content = content + '<div class = "ct-content" style = "font-size:14px;">  <div class = "circle" style="background-color:'+info.event.backgroundColor+';float:left;"></div> &nbsp;&nbsp;&nbsp;' + info.event.extendedProps.type + '</div>'

            }
            content = content + '<div class = "ct-content">' + description + '</div><br>'
            content = content + '<div style = "height:10px;"> . </div></div>'
            
            tippy(info.el, {
                appendTo: document.body,
                placement: 'bottom',
                animation: 'fade',
                theme: 'transparent',
                trigger: 'click',
                allowHTML: true,
                interactive: false,
                arrow : false,
                content: content

            
            }); // tippy end
            },
        events: function (fetchInfo, successCallback, failureCallback) {
            var events_fc = [];

            var events = vacs.concat(tasks);

            for (var i in events){
                var event = events[i];


                events_fc.push(
                    {
                    groupId : event.id,
                    backgroundColor: event.color,
                    borderColor : event.color,
                    title: event.title,
                    type: event.type,
                    start: event.start,
                    end: event.end,
                    allDay : event.allday,//event.allday,
                    description : event.description,
                    users : event.users,
                    overlap : 'false'
                    })
                };

                successCallback(events_fc); // event end
                }

            });
        calendar.render();

        for (var i = 0; i < checkbox.length; i++) {

            checkbox[i].addEventListener('change', function() {
                calendar.refetchEvents();
                });
            console.log('added');
        }
    });

// 이벤트 타입별 색 변환
$(document).ready(function () {
    for(var key in task_colors_json){
        var el = document.getElementById("label_" + task_colors_json[key]);
        el.style["background-color"] =  task_colors_json[key];
        el.style["border-color"] =  task_colors_json[key];
        };
    for(var key in vac_colors_json){
        var el = document.getElementById("label_" + vac_colors_json[key]);
        el.style["background-color"] =  vac_colors_json[key];
        el.style["border-color"] =  vac_colors_json[key];
        };

    });


// 툴바 너비 변경
window.onload = function () {
    $('fc-toolbar.fc-toolbar-ltr').addClass('row col-lg-12');
}; 



// form to dictionary 
function parse_forms(form) {
    var dict = {};
    var children = $(form).children('input');
    console.log(children);
    for (var i = 0; i < children.length; i ++){
        dict[ $(children[i]).prop('id') ] = $(children[i]).val();
        };

    dict['type'] = $(form).children('div').text();
    console.log(dict);
    return dict

    }   