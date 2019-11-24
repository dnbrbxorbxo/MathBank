// DataTables 함수에 들어갈 매개 변수.
function dataTables(datas, labels, pageLength) {
    value = {
        lengthChange: false,
        info: false,
        "pageLength": pageLength,

        data: datas,
        columns: labels
    };
    return value;
}

window.onload = function () {
    var column;
    if (entity == 'location') column = [{title: "개체명"}, {title: "횟수"}];
    else if (entity == 'entity') column = [{title: "위치"}, {title: "횟수"}];
    console.log(column)

    var pageLength = 8;

    $(document).ready( function() {
        $('#datatable').DataTable(dataTables(result, column, pageLength));
    } );
}