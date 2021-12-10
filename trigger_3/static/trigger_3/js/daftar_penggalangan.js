var detailButtons = document.getElementsByClassName("detail_button");
[].slice.call(detailButtons).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/t3/detail-penggalangan?id=" + id_penggalangan;
    };
});

var verifikasiButtons = document.getElementsByClassName("verifikasi_button");
[].slice.call(verifikasiButtons).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/verifikasi-penggalangan?id=" + id_penggalangan;
    }
})

var donasiButton = document.getElementsByClassName("donasi_button");
[].slice.call(donasiButton).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/t4/create-donasi?id=" + id_penggalangan;
    }
})