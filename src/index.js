// 캘린더를 생성하기 위해 tui-calendar 객체와 스타일 코드 삽입
import Calendar from 'tui-calendar';
import 'tui-calendar/dist/tui-calendar.css';
import 'tui-date-picker/dist/tui-date-picker.css';
import 'tui-time-picker/dist/tui-time-picker.css';

const container = document.getElementById('calendar');
const options = {
  defaultView: 'week',          // 캘린더가 초기에 그려지는 뷰 타입을 주간 뷰로 지정
  week: {                       // 주간 뷰 시간 지정
    hourStart: 7,
    hourEnd: 18
  }
};

const calendar = new Calendar(container, options);  // 캘린더 인스턴스 생성


nextBtn.addEventListener('click', () => {
  calendar.next();                          // 현재 뷰 기준으로 다음 뷰로 이동
});

prevBtn.addEventListener('click', () => {
  calendar.prev();                          // 현재 뷰 기준으로 이전 뷰로 이동
});

dayViewBtn.addEventListener('click', () => {
  calendar.changeView('day', true);         // 일간 뷰 보기
});

weekViewBtn.addEventListener('click', () => {
  calendar.changeView('week', true);        // 주간 뷰 보기
});

monthViewBtn.addEventListener('click', () => {
  calendar.changeView('month', true);       // 월간 뷰 보기
});