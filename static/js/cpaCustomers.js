// insert data to view

// List users tab
function loadListUsersAdminCus() {
  let listUsersApi = "";
  document.getElementById("ListUsersAdmin3").innerHTML = "";
  if (listCus.id_cliente.length == 0) {
    document.getElementById("ListUsersAdmin3").innerHTML = `
      <h4 class="text-center text-dark d-block">No hay clientes</h4>
      `;
  } else {
    for (let i = 0; i < listCus.id_cliente.length; i++) {
      listUsersApi += `<div class="d-block text-center text-dark">
            <span class="d-inline-block w-x">${listCus.nombres[i]} ${
        listCus.apellidos[i]
      }</span>
            <span class="d-inline-block w-x">${listCus.alias[i]}</span>
            <span class="d-inline-block w-x">${listCus.correo[i]}</span>
            <span class="d-inline-block w-x">${
              listCus.nombre_producto_asociado[i]
            }</span>
            <span class="d-inline-block w-x">${
              listCus.precio_producto_asociado[i]
            }</span>${
        listCus.estado_cliente[i] == 1
          ? `<span class="d-inline-block w-x">En servicio <i class="fas fa-circle text-success optionsBarUserAdmin" title="Cliente activo"></i></span>`
          : `<span class="d-inline-block w-x">Sin servicio <i class="fas fa-circle text-danger optionsBarUserAdmin" title="Cliente inactivo"></i></span>`
      }
    <span class="d-inline-block w-x">
    <i class="far fa-edit text-primary optionsBarUserAdmin" title="Editar cliente"></i>
        <form class="d-inline" action="#">
                <input type="hidden" name="id_registro" value="${
                  listCus.id_cliente[i]
                }">
                <i class="far fa-trash-alt text-danger optionsBarUserAdmin d-inline sty1-list-usr-md-cpadmin" title="Borrar cliente" onclick="deleteRegCusLu(this.parentNode)"></i>
        </form>
        </div>
        <hr>`;
    }
    document.getElementById("ListUsersAdmin3").innerHTML = listUsersApi;
  }
}

// insert products available
function addProductsSelectList() {
  let list = `<option hidden selected value="">Seleccione un producto</option>`;
  if (listProds.nombres.length == 0) {
    document.getElementById(
      "ListProductsSelect"
    ).innerHTML = `<option hidden selected value="">No hay productos</option>`;
  } else {
    for (let i = 0; i < listProds.nombres.length; i++) {
      list += `<option value="${listProds.id[i]}">${listProds.nombres[i]}</option>`;
    }
    document.getElementById("ListProductsSelect").innerHTML = list;
  }
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
  } else if ($("#ListProductsSelect").val() == 0) {
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
      listCus = info;
      runAllBeforeUpdate();
      $("#formSubmitCus")[0].reset();
      console.log(info);
      $("#alertPrimarySystem").html(`Cliente guardado!`).fadeIn();
      setTimeout(function () {
        $("#alertPrimarySystem").fadeOut();
      }, 2000);
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

// set date now
let dateNow = new Date();
let fechaDeHoy = document.querySelector("#fechaDeHoy");
fechaDeHoy.innerHTML = `
${dateNow.getDate().toString().padStart(2, 0)}/${(dateNow.getMonth() + 1)
  .toString()
  .padStart(2, 0)}/${dateNow.getFullYear().toString()}
`;
