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

            tippy(info.el, {
                animation: 'fade',
                theme: 'material',
                trigger: 'click',
                allowHTML: true,
                interactive: true,
                content: '<div> [담당자] ' + users + '</div><br><div> [내용] ' + description + '</div><br><div> [기간] ' + start + ' ~ ' + end + ' </div>', //info.event.extendedProps.description
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
                    start: event.start,
                    end: event.end,
                    allDay : event.allday,
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


    // so your code will be



// 메세지 timeout
window.setTimeout(function() {
    $(".alert-auto-dismissible").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
        });
    }, 2000);

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


$(document).ready(function(){
    $(".delete").on('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = $(this).data('uri');
        }
    });
});



// 견적서 추가항목 작성 로직
// 이렇게 해도 되는건가.. ? 작동은 하는데..
// 아래 항목이 아닌 위 항목을 지우면 번호가 자동으로 땡겨져야 함

var x = 1;

$('#add-button').click(function() {
    var wrapper = $('#form123')
    var structure = $('<div class="form-group"><label for = "additional_' + x + '">추가항목 ' + x + '</label><br/><div style = "width: 20%;float:left;">항목 이름 &nbsp;: &nbsp;&nbsp;</div><input class="form-control" type="text" style = "width:auto;" name="additional_key' + x + '"><br/><div style = "width: 15%;float:left;"> 가격 &nbsp;: &nbsp;&nbsp;</div><input class="form-control" type="text" style = "width: auto;" name="additional_val' + x +  '"><br><a href="#" class="delete" id = "delete'+x+'">삭제</a></div>');
    var submit_btn = $('#submit')

    $(submit_btn).before(structure);

    x++;
    //off 안하면 페이지 안에서의 누적클릭횟수만큼 반복해서 발생함
    $(wrapper).off().on("click", ".delete", function(e) {
        e.preventDefault();
        $(this).parent('div').remove();
        x--;
    });
});

// 검색 및 페이지 이동

$(document).ready(function(){
    $(".page-link").on('click', function() {
        $("#page").val($(this).data("page"));
        $("#searchForm").submit();
    });

    $("#btn_search").on('click', function() {
        $("#kw").val($(".kw").val());
        $("#page").val(1);  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
        $("#searchForm").submit();
    });
});

// 프로필 수정. form에 사용자 정보를 넣기 위해 form에서 표시는 하지만
// 편집은 못하게 disabled 처리하면 form.is_valid()를 통과 못함.
// 제출 시 해제
$('#usermodify').submit(function(){
    $("#usermodify :disabled").removeAttr('disabled');
});




window.onload = function () {
    $('fc-toolbar.fc-toolbar-ltr').addClass('row col-lg-12');
};



