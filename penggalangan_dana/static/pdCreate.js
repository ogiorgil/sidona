let listKategori = [];
$.get("/pd/kategori/", (data, status) => {
  if (status !== "success") return;
  listKategori = data.kategori;
  console.log(listKategori);
});

let kategoriPd;
let nikPasien, namaPasien, tanggalLahirPasien, alamatPasien, pekerjaanPasien;
let sertifikatRumahIbadah, namaRumahIbadah, alamatRumahIbadah, jenisRumahIbadah;

$(document).ready(() => {
  $("#formPd").hide();
  $("#formPd").find("#formPdKesehatan").hide();
  $("#formPd").find("#formPdRumahIbadah").hide();

  $("#cekPasien").hide();
  $("#formPasien").hide();
  $("#dialogTambahPasien").hide();

  $("#cekRumahIbadah").hide();
  $("#formRumahIbadah").hide();
  $("#dialogTambahRumahIbadah").hide();

  $("#formKategoriPd").show();

  // Section pilih kategori
  $("#kategoriPdNextButton").click(() => {
    kategoriPd = $("#kategoriPdSelect").val();
    kategoriPd = listKategori.find((k) => k.id == kategoriPd);

    // Generate id baru untuk penggalangan dana
    $.post(
      "/pd/generate-id/",
      {
        id_kategori_pd: kategoriPd.id,
        alias_kategori_pd: kategoriPd.alias,
      },
      (data, status) => {
        if (status !== "success") return;
        $("#pdIdInput").val(data.id);
      }
    );

    // Masukkan nama kategori pada form
    $("#pdKategoriInput").val(kategoriPd.id);
    $("#pdNamaKategori").val(kategoriPd.nama);

    // Jika kategori "Kesehatan", tampilkan pemilihan Pasien
    if (kategoriPd === "2") {
      $("#formKategoriPd").hide();
      $("#dialogTambahPasien").show();
    } else if (kategoriPd === "1") {
      $("#formKategoriPd").hide();
      $("#dialogTambahRumahIbadah").show();
    } else {
      $("#formKategoriPd").hide();
      $("#formPd").show();
    }
  });

  // Section dialog tambah Pasien
  $("#dialogTambahPasien")
    .find("#yaButton")
    .click(() => {
      $("#dialogTambahPasien").hide();
      $("#formPasien").show();
    });

  $("#dialogTambahPasien")
    .find("#tidakButton")
    .click(() => {
      $("#dialogTambahPasien").hide();
      $("#cekPasien").show();
    });

  // Section form Pasien
  $("#pasienNextButton").click(() => {
    nikPasien = $("pasienNikInput").text();
    namaPasien = $("pasienNamaInput").text();
    tanggalLahirPasien = $("pasienTanggalLahirInput").text();
    alamatPasien = $("pasienAlamatInput").text();
    pekerjaanPasien = $("pasienPekerjaanInput").text();

    $("#formPasien").hide();
    $("#formPd").show();
    $("#formPd").find("#formPdKesehatan").show();
  });

  // Section cek Pasien
  $("#cekPasienNextButton").click(() => {
    $("#cekPasien").hide();
    $("#formPd").show();
    $("#formPd").find("#formPdKesehatan").show();
  });

  // Section dialog tambah Rumah Ibadah
  $("#dialogTambahRumahIbadah")
    .find("#yaButton")
    .click(() => {
      $("#dialogTambahRumahIbadah").hide();
      $("#formRumahIbadah").show();
    });

  $("#dialogTambahRumahIbadah")
    .find("#tidakButton")
    .click(() => {
      $("#dialogTambahRumahIbadah").hide();
      $("#cekRumahIbadah").show();
    });

  // Section form Rumah Ibadah
  $("#rumahIbadahNextButton").click(() => {
    sertifikatRumahIbadah = $("rumahIbadahSertifikatInput").text();
    namaRumahIbadah = $("rumahIbadahNamaInput").text();
    alamatRumahIbadah = $("rumahIbadahAlamatInput").text();
    jenisRumahIbadah = $("rumahIbadahJenisInput").text();

    $("#formRumahIbadah").hide();
    $("#formPd").show();
    $("#formPd").find("#formPdRumahIbadah").show();
  });

  //Section cek Rumah Ibadah
  $("#cekRumahIbadahNextButton").click(() => {
    $("#cekRumahIbadah").hide();
    $("#formPd").show();
    $("#formPd").find("#formPdRumahIbadah").show();
  });
});
