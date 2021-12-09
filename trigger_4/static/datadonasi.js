var detailButtons = document.getElementsByClassName("detail_button");
[].slice.call(detailButtons).forEach(function (button) {
    button.onclick = function () {
        let email_pengguna = button.id.slice(14,21);
        let timestamp = button.id.slice(22,)
        location.href = "/detail-donasi?email=" + email_pengguna +"&timestamp="+timestamp;
    };
});