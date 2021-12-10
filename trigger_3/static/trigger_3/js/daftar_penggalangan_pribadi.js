var detailButtons = document.getElementsByClassName("update_button");
[].slice.call(detailButtons).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/t3/update-penggalangan?id=" + id_penggalangan;
    };
});
