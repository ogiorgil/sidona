var detailButtons = document.getElementsByClassName("detail_button");
[].slice.call(detailButtons).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/detail-penggalangan?id=" + id_penggalangan;
    };
});