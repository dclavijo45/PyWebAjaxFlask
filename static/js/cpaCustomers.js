// insert data to view

// List users tab
function loadListUsersAdminCus() {}

// insert products available
function addProductsSelectList() {
  let list = `<option hidden selected value="">Seleccione un producto</option>`;
  for (let i = 0; i < listProds.nombres.length; i++) {
    list += `<option value="${listProds.id[i]}">${listProds.nombres[i]}</option>`;
  }
  document.getElementById("ListProductsSelect").innerHTML = list;
}

// run functions for add data
function runAllBeforeUpdate() {
  loadListUsersAdminCus();
  addProductsSelectList();
}

runAllBeforeUpdate();

// set config to add reg
$("#btnAddReg").click(function (e) {
  if ($("#BoxLabelsListUsersReg").is(":visible")) {
    $("#BoxLabelsListUsersReg").hide();
    $("#BoxLabelsAddReg").show();
    $("#ListUsersAdmin3").hide();
    $("#BoxAddReg").show();
  } else {
    $("#BoxLabelsListUsersReg").show();
    $("#BoxLabelsAddReg").hide();
    $("#ListUsersAdmin3").show();
    $("#BoxAddReg").hide();
  }
});

//set btn to events add customer
$("#btnNotSaveRegistercpa").click(function (e) {
  if (!$("#BoxLabelsListUsersReg").is(":visible")) {
    if (confirm("Descartar algun cambio?")) {
      $("#formSubmitCus")[0].reset();
      $("#BoxLabelsListUsersReg").show();
      $("#BoxLabelsAddReg").hide();
      $("#ListUsersAdmin3").show();
      $("#BoxAddReg").hide();
    } else {
      return false;
    }
  } else {
    return false;
  }
});

// Delete register event !
function deleteRegCusLu() {
  if (confirm("Seguro desea borrar al cliente?")) {
    let action = "/apicus";
    let method = "DELETE";
    $.ajax({
      beforeSend: function (xhr, settings) {
        // if (
        //   !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
        //   !this.crossDomain
        // ) {
        //   xhr.setRequestHeader("X-CSRFToken", csrf_token);
        // }
      },
      url: action,
      type: method,
      data: JSON.stringify({
        id_registro: form.elements[0].value,
      }),
      dataType: "json",
      success: function (info) {
        $("#alertPrimarySystem").html(`Cliente borrado!`).fadeIn();
        setTimeout(function () {
          $("#alertPrimarySystem").fadeOut();
        }, 2000);
        runAllBeforeUpdate();
      },
      error: function (jqXHR, status, error) {
        $("#alertDangerSystem")
          .html(
            `Cliente no borrado, por favor informe a la administración el problema`
          )
          .fadeIn();
        setTimeout(function () {
          $("#alertDangerSystem").fadeOut();
        }, 2000);
        console.log(`Estado: ${status}`);
        console.log(`Error: ${error}`);
      },
      timeout: 10000,
    });
  }
}

// Add cliente event !

$("#btnSaveRegistercpa").click((e) => {
  e.preventDefault();
  if ($("#nombreClienteInput").val() == 0) {
    $("#alertDangerSystem").html(`Escriba el nombre!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  } else if ($("#apellidoClienteInput").val() == 0) {
    $("#alertDangerSystem").html(`Escriba los apellidos!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  } else if ($("#tipoIdClienteSelect").val() == 0) {
    $("#alertDangerSystem").html(`Selecciona un tipo de documento!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  } else if ($("#numDocumentoClienteInput").val() == 0) {
    $("#alertDangerSystem").html(`Escriba el número de documento!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  } else if ($("#listProductsSelect").val() == 0) {
    $("#alertDangerSystem").html(`Selecciona un producto!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  }
  $.ajax({
    beforeSend: function (xhr, settings) {
      // if (
      //   !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
      //   !this.crossDomain
      // ) {
      //   xhr.setRequestHeader("X-CSRFToken", csrf_token);
      // }
      console.clear();
      console.log("Consultado...");
    },
    url: "/apicus",
    type: "POST",
    data: JSON.stringify(
      $("#BoxAddReg form")
        .serializeArray()
        .reduce(function (a, z) {
          a[z.name] = z.value;
          return a;
        }, {})
    ),
    dataType: "json",
    success: function (info) {
      $("#formSubmitCus")[0].reset();
      console.log(info);
      $("#alertPrimarySystem").html(`Cliente guardado!`).fadeIn();
      setTimeout(function () {
        $("#alertPrimarySystem").fadeOut();
      }, 2000);

      runAllBeforeUpdate();
    },
    error: function (jqXHR, status, error) {
      $("#alertDangerSystem")
        .html(
          `Cliente no guardado, por favor informe a la administración el problema`
        )
        .fadeIn();
      setTimeout(function () {
        $("#alertDangerSystem").fadeOut();
      }, 2000);
      console.log(`Estado: ${status}`);
      console.log(`Error: ${error}`);
    },
    timeout: 10000,
  });
});

// manage when the user press enter
$("#IARquantity").on("keydown", function (e) {
  if (e.which == 13) {
    $("#btnSaveRegistercpa").click();
  }
});

// Fix list users qnt
if (userinfo.customers.total == 0)
  document.getElementById(
    "ListUsersAdmin2"
  ).innerHTML = `<h4 class="text-center text-dark d-block">No hay clientes</h4>`;

// set date now
let dateNow = new Date();
let fechaDeHoy = document.querySelector("#fechaDeHoy");
fechaDeHoy.innerHTML = `
${dateNow.getDate().toString().padStart(2, 0)}/${(dateNow.getMonth() + 1)
  .toString()
  .padStart(2, 0)}/${dateNow.getFullYear().toString()}
`;
