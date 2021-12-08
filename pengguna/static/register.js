let jenisAkun, jenisPd;

const setAdminRequired = (isRequired) => {
  $("#adminEmailInput").prop("required", isRequired);
  $("#adminPasswordInput").prop("required", isRequired);
  $("#adminNamaInput").prop("required", isRequired);
  $("#adminNoHpInput").prop("required", isRequired);
};

const setPdRequired = (isRequired) => {
  $("#pdEmailInput").prop("required", isRequired);
  $("#pdPasswordInput").prop("required", isRequired);
  $("#pdNamaInput").prop("required", isRequired);
  $("#pdNoHpInput").prop("required", isRequired);
  $("#pdAlamatInput").prop("required", isRequired);
  $("#pdNamaBankInput").prop("required", isRequired);
  $("#pdNomorRekeningInput").prop("required", isRequired);
}

const setIndividuRequired = (isRequired) => {
  $("#pdiNikInput").prop("required", isRequired);
  $("#pdiTanggalLahirInput").prop("required", isRequired);
  $("#pdiJenisKelaminInput").prop("required", isRequired);
  $("#pdiKtpInput").prop("required", isRequired);
};

const setOrganisasiRequired = (isRequired) => {
  $("#pdoNamaInput").prop("required", isRequired);
  $("#pdoNoTelpInput").prop("required", isRequired);
  $("#pdoTahunInput").prop("required", isRequired);
  $("#pdoNomorAktaInput").prop("required", isRequired);
  $("#pdoFotoAktaInput").prop("required", isRequired);
};

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
      $("#pdiSection").hide();
      $("#pdoSection").hide();
      $("#adminSection").show();

      setPdRequired(false);
      setIndividuRequired(false);
      setOrganisasiRequired(false);
      setAdminRequired(true);
    } else if (jenisAkun === "Penggalang Dana") {
      $("#adminSection").hide();
      $("#pdiSection").hide();
      $("#pdoSection").hide();
      $("#pdSection").show();

      setAdminRequired(false);
      setIndividuRequired(false);
      setOrganisasiRequired(false);
      setPdRequired(true);
    }
  });

  $("#pdButton").click(() => {
    jenisPd = $("#pdJenisSelect").find(":selected").text();

    if (jenisPd === "Individu") {
      $("#pdoSection").hide();
      $("#pdiSection").show();

      setAdminRequired(false);
      setOrganisasiRequired(false);
      setPdRequired(true);
      setIndividuRequired(true);
    } else if (jenisPd === "Organisasi") {
      $("#pdiSection").hide();
      $("#pdoSection").show();

      setAdminRequired(false);
      setIndividuRequired(false);
      setPdRequired(true);
      setOrganisasiRequired(true);
    }
  });
});
