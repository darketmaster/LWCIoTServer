$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        pageLength: 40,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "ip"},
            {"data": "mac"},
            {"data": "mq135"},
            {"data": "sds011"},
            {"data": "ordate"},
            {"data": "redate"}
        ],
        initComplete: function (settings, json) {

        }
    });
});