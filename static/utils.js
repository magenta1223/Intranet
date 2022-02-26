// 메세지 timeout
window.setTimeout(function() {
    $(".alert-auto-dismissible").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
        });
    }, 2000);



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



