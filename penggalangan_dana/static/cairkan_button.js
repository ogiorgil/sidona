var cairkanButtons = document.getElementsByClassName("cairkan_button");
[].slice.call(cairkanButtons).forEach(function (button) {
    button.onclick = function () {
        let id_penggalangan = button.id.slice(-5);
        location.href = "/pencairan-dana?id=" + id_penggalangan;
    };
});