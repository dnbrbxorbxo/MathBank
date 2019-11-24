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
    var column = [{title: "개체명"}, {title: "횟수"}];
    var pageLength = 5;

    $(document).ready( function() {
        $('#attraction').DataTable(dataTables(attraction, column, pageLength));
    } );

    $(document).ready( function() {
        $('#travel').DataTable(dataTables(travel, column, pageLength));
    } );

    $(document).ready( function() {
        $('#restaurant').DataTable(dataTables(restaurant, column, pageLength));
    } );

    $(document).ready( function() {
        $('#weather').DataTable(dataTables(weather, column, pageLength));
    } );

    $(document).ready( function() {
        $('#dust').DataTable(dataTables(dust, column, pageLength));
    } );
}