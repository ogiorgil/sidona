let jenisAkun, jenisPd;

$(document).ready(() => {
  // Hide unused form sections.
  $("#adminSection").hide();
  $("#pdSection").hide();
  $("#pdiSection").hide();
  $("#pdoSection").hide();

  $("#jenisAkunButton").click(() => {
    jenisAkun = $("#jenisAkunSelect").find(":selected").text();

    if (jenisAkun === "Admin") {
      $("#pdSection").hide();
      $("#adminSection").show();
    } else if (jenisAkun === "Penggalang Dana") {
      $("#adminSection").hide();
      $("#pdSection").show();
    }
  });

  $("#pdButton").click(() => {
    jenisPd = $("#pdJenisSelect").find(":selected").text();

    if (jenisPd === "Individu") {
      $("#pdoSection").hide();
      $("#pdiSection").show();
    } else if (jenisPd === "Organisasi") {
      $("#pdiSection").hide();
      $("#pdoSection").show();
    }
  });
});
