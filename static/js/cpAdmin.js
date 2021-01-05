// insert data to view

// declarations
let clientesAlcanzados = [];
let capitalTotalCus1 = 0;
let volumenProductoTotalCus1 = 0;
let ListUsersAdmin = "";
let diaRegistradoListUACus = "";
let datosSemanaActual = [0, 0, 0, 0, 0, 0, 0];
let datosSemanaPasada = [0, 0, 0, 0, 0, 0, 0];
let selectorOpcionesCustomers = "";

// chart config
let chartColors = {
  red: "rgb(255, 99, 132)",
  orange: "rgb(255, 159, 64)",
  yellow: "rgb(255, 205, 86)",
  green: "rgb(75, 192, 192)",
  blue: "rgb(54, 162, 235)",
  purple: "rgb(153, 102, 255)",
  grey: "rgb(201, 203, 207)",
};
let config = {
  type: "bar",
  data: {
    labels: [
      "Lunes",
      "Martes",
      "Miercoles",
      "Jueves",
      "Viernes",
      "Sabado",
      "Domingo",
    ],
    datasets: [
      {
        label: "Semana actual",
        borderColor: chartColors.orange,
        backgroundColor: chartColors.red,
        data: datosSemanaActual,
      },
      {
        label: "Semana pasada",
        borderColor: chartColors.purple,
        backgroundColor: chartColors.blue,
        data: datosSemanaPasada,
      },
    ],
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: "Estado de ventas",
    },
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "index",
    },
    scales: {
      xAxes: [
        {
          scaleLabel: {
            stacked: true,
            display: true,
            labelString: "Dias",
          },
        },
      ],
      yAxes: [
        {
          stacked: true,
          scaleLabel: {
            display: true,
            labelString: "Cantidad",
          },
        },
      ],
    },
  },
};

// add chart
let ctx = document.getElementById("canvas").getContext("2d");
let myLine = new Chart(ctx, config);

// clientes box
function loadClientesBox() {
  try {
    for (
      let i = 0;
      i <= userinfo.reports.current_week.id_customer.length;
      i++
    ) {
      //console.log(i);
      for (let j = 0; j < userinfo.customers.id.length; j++) {
        if (
          userinfo.reports.current_week.id_customer[i] ==
            userinfo.customers.id[j] &&
          clientesAlcanzados.includes(
            userinfo.reports.current_week.id_customer[i]
          ) == false
        ) {
          clientesAlcanzados.push(userinfo.reports.current_week.id_customer[i]);
        }
      }
    }
  } catch (e) {
    console.log("No data received");
  }

  document.getElementById("qntCustomersAlcn").innerHTML =
    clientesAlcanzados.length;

  if (clientesAlcanzados.length == 0 && userinfo.customers.total == 0) {
    document.getElementById(
      "porcentajeCus1Alcn"
    ).innerHTML = `restante ${clientesAlcanzados.length}/${userinfo.customers.total} - 0%`;
  } else {
    document.getElementById("porcentajeCus1Alcn").innerHTML = `restante ${
      clientesAlcanzados.length
    }/${userinfo.customers.total} - ${(
      (clientesAlcanzados.length * 100) /
      userinfo.customers.total
    ).toFixed(2)}%`;
  }
}

// capital total box
function loadTotalCapitalBox() {
  try {
    for (
      let i = 0;
      i < userinfo.reports.current_week.precio_producto_vendido.length;
      i++
    ) {
      capitalTotalCus1 +=
        userinfo.reports.current_week.precio_producto_vendido[i];
    }
    let capitalTotalCus1Format = capitalTotalCus1.toString().split("");
    let count1 = -1;
    let capitalTotalCus1Format2 = [];
    for (let i = capitalTotalCus1Format.length; i >= 0; i--) {
      if (count1 % 3 == 0 && count1 != 0) {
        capitalTotalCus1Format2.push(".");
      }
      capitalTotalCus1Format2.push(capitalTotalCus1Format[i]);
      count1++;
    }

    let capitalTotalCus1Format3 = capitalTotalCus1Format2.join("");
    let capitalTotalCus1Format4 = "";

    for (var i = capitalTotalCus1Format3.length - 1; i >= 0; i--) {
      capitalTotalCus1Format4 += capitalTotalCus1Format3[i];
    }

    document.getElementById(
      "capitalTotalCus1"
    ).innerHTML = `$${capitalTotalCus1Format4}`;
  } catch (e) {
    document.getElementById("capitalTotalCus1").innerHTML = `$0`;
  }
}

// volumen box
function loadVolumenBox() {
  try {
    for (let i = 0; i < userinfo.reports.current_week.volumen.length; i++) {
      volumenProductoTotalCus1 += userinfo.reports.current_week.volumen[i];
    }
    document.getElementById(
      "volumenProductoTotalCus1"
    ).innerHTML = volumenProductoTotalCus1;
  } catch (e) {
    document.getElementById("volumenProductoTotalCus1").innerHTML = 0;
  }
}

// List users tab
function loadListUsersAdminCus() {
  let precioDePagoPorCus = 0;
  try {
    for (let i = 0; i < userinfo.reports.current_week.id_reporte.length; i++) {
      if (userinfo.reports.current_week.report_date[i].slice(0, 3) == "Mon") {
        diaRegistradoListUACus = "Lunes";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Tue"
      ) {
        diaRegistradoListUACus = "Martes";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Wed"
      ) {
        diaRegistradoListUACus = "Miercoles";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Thu"
      ) {
        diaRegistradoListUACus = "Jueves";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Fri"
      ) {
        diaRegistradoListUACus = "Viernes";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Sat"
      ) {
        diaRegistradoListUACus = "Sabado";
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Sun"
      ) {
        diaRegistradoListUACus = "Domingo";
      } else {
        console.error(
          `Has ocurred a error, received: ${userinfo.reports.current_week.report_date[
            i
          ].slice(0, 3)}`
        );
      }

      for (let j = 0; j < userinfo.customers.id.length; j++) {
        if (
          userinfo.reports.current_week.id_customer[i] ==
          userinfo.customers.id[j]
        ) {
          precioDePagoPorCus = userinfo.customers.precio_pago_prod[j];
          break;
        }
      }

      ListUsersAdmin += `
    <div class="d-block">
            <h6 class="text-center list-usr-md-cpadmin" title="Precio: ${precioDePagoPorCus}">${
        userinfo.reports.current_week.name[i]
      }</h6>
            <h6 class="text-muted text-center list-usr-md-cpadmin">${diaRegistradoListUACus}/${userinfo.reports.current_week.report_date[
        i
      ].slice(5, 7)}/${userinfo.reports.current_week.report_date[i].slice(
        14,
        16
      )}</h6>
            <h6 class="text-center list-usr-md-cpadmin">${
              userinfo.reports.current_week.volumen[i]
            }</h6>
            <h6 class="text-center d-inline-block">${
              userinfo.reports.current_week.precio_producto_vendido[i]
            }</h6>
            <h6 class="text-center btn-edt-reg-cpadmin">
                <i class="far fa-edit text-primary optionsBarUserAdmin" title="Editar registro sty1-list-usr-md-cpamin"></i>
                    <form class="d-inline" action="/apirf">
                    <input type="hidden" name="id_registro" value="${
                      userinfo.reports.current_week.id_reporte[i]
                    }">
                <i class="far fa-trash-alt text-danger optionsBarUserAdmin d-inline sty1-list-usr-md-cpadmin" title="Borrar registro" onclick="deleteRegCusLu(this.parentNode)"></i>
                    </form>
            </h6>
        </div>
        <hr>
    `;
    }
    document.getElementById("ListUsersAdmin").innerHTML = ListUsersAdmin;
  } catch (e) {
    console.log(e);
    document.getElementById(
      "ListUsersAdmin"
    ).innerHTML = `<h4 class="text-center text-dark d-block">No hay clientes</h4>`;
  }
}

// chart all

// current week data
function loadCurrentWeekData() {
  try {
    for (let i = 0; i < userinfo.reports.current_week.report_date.length; i++) {
      if (userinfo.reports.current_week.report_date[i].slice(0, 3) == "Mon") {
        datosSemanaActual[0] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Tue"
      ) {
        datosSemanaActual[1] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Wed"
      ) {
        datosSemanaActual[2] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Thu"
      ) {
        datosSemanaActual[3] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Fri"
      ) {
        datosSemanaActual[4] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Sat"
      ) {
        datosSemanaActual[5] += userinfo.reports.current_week.volumen[i];
      } else if (
        userinfo.reports.current_week.report_date[i].slice(0, 3) == "Sun"
      ) {
        datosSemanaActual[6] += userinfo.reports.current_week.volumen[i];
      } else {
        console.error(
          `Has ocurred a error, received: ${userinfo.reports.current_week.report_date[
            i
          ].slice(0, 3)}`
        );
      }
    }
  } catch (e) {
    console.log("Not found current report");
  }
}

// last week data
function loadLastWeekData() {
  try {
    for (let i = 0; i < userinfo.reports.last_week.report_date.length; i++) {
      if (userinfo.reports.last_week.report_date[i].slice(0, 3) == "Mon") {
        datosSemanaPasada[0] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Tue"
      ) {
        datosSemanaPasada[1] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Wed"
      ) {
        datosSemanaPasada[2] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Thu"
      ) {
        datosSemanaPasada[3] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Fri"
      ) {
        datosSemanaPasada[4] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Sat"
      ) {
        datosSemanaPasada[5] += userinfo.reports.last_week.volumen[i];
      } else if (
        userinfo.reports.last_week.report_date[i].slice(0, 3) == "Sun"
      ) {
        datosSemanaPasada[6] += userinfo.reports.last_week.volumen[i];
      } else {
        console.error(
          `Has ocurred a error, received: ${userinfo.reports.last_week.report_date[
            i
          ].slice(0, 3)}`
        );
      }
    }
  } catch (e) {
    console.log("Not found last report");
  }
  myLine.update();
}

// set options on add register customers
function loadOptionsSelectorCus() {
  selectorOpcionesCustomers = `<option selected hidden value="">Seleccionar</option>`;
  try {
    for (let i = 0; i < userinfo.customers.name.length; i++) {
      selectorOpcionesCustomers += `
        <option value="${userinfo.customers.id[i]}">${userinfo.customers.name[i]}</option>
        `;
    }
  } catch (e) {
    console.log("Customers not found");
  }

  document.getElementById(
    "selectorOpcionesCustomers"
  ).innerHTML = selectorOpcionesCustomers;
}

// run functions for add data
loadClientesBox();
loadTotalCapitalBox();
loadVolumenBox();
loadListUsersAdminCus();
loadCurrentWeekData();
loadLastWeekData();
loadOptionsSelectorCus();

function runAllBeforeUpdate() {
  clientesAlcanzados = [];
  capitalTotalCus1 = 0;
  volumenProductoTotalCus1 = 0;
  ListUsersAdmin = "";
  diaRegistradoListUACus = "";
  datosSemanaActual = [0, 0, 0, 0, 0, 0, 0];
  datosSemanaPasada = [0, 0, 0, 0, 0, 0, 0];
  selectorOpcionesCustomers = "";
  loadClientesBox();
  loadTotalCapitalBox();
  loadVolumenBox();
  loadListUsersAdminCus();
  loadCurrentWeekData();
  loadLastWeekData();
  loadOptionsSelectorCus();
  config.data.datasets[0].data = datosSemanaActual;
  config.data.datasets[1].data = datosSemanaPasada;
  myLine.update();
}

// set config to add reg
$("#btnAddReg").click(function (e) {
  if ($("#ListUsersAdmin").is(":visible")) {
    $("#ListUsersAdmin").hide();
    $("#BoxAddReg").show();
    $("#BoxLabelsListUsersReg").hide();
    $("#BoxLabelsAddReg").show();
  } else {
    $("#BoxLabelsAddReg").hide();
    $("#BoxLabelsListUsersReg").show();
    $("#ListUsersAdmin").show();
    $("#BoxAddReg").hide();
  }
});

// set date now cpAdmin input date and table L-Ucus info
let dateNow = new Date();
let field = document.querySelector("#datenow");
let fechaDeHoy = document.querySelector("#fechaDeHoy");

field.value =
  dateNow.getFullYear().toString() +
  "-" +
  (dateNow.getMonth() + 1).toString().padStart(2, 0) +
  "-" +
  dateNow.getDate().toString().padStart(2, 0);
fechaDeHoy.innerHTML = `
${dateNow.getDate().toString().padStart(2, 0)}/${(dateNow.getMonth() + 1)
  .toString()
  .padStart(2, 0)}/${dateNow.getFullYear().toString()}
`;

// setup input price product as not change
$("#InputPricecpa").change(function (e) {
  e.preventDefault();
});
$("#InputPricecpa").keydown(function (e) {
  e.preventDefault();
});
$("#InputPricecpa").click(function (e) {
  e.preventDefault();
});

//set btn to events add register
$("#btnNotSaveRegistercpa").click(function (e) {
  if ($("#ListUsersAdmin").is(":visible")) {
    $("#ListUsersAdmin").hide();
    $("#BoxAddReg").show();
    $("#BoxLabelsListUsersReg").hide();
    $("#BoxLabelsAddReg").show();
  } else {
    $("#BoxLabelsAddReg").hide();
    $("#BoxLabelsListUsersReg").show();
    $("#ListUsersAdmin").show();
    $("#BoxAddReg").hide();
  }
});

// set price in event to change of customer
$("#selectorOpcionesCustomers").change(function (e) {
  $("#InputPricecpa").attr(
    "value",
    userinfo.customers.precio_pago_prod[
      document.getElementById("selectorOpcionesCustomers").selectedIndex - 1
    ]
  );
});

// Delete register event !
function deleteRegCusLu(form) {
  if (confirm("Borrar este registro?")) {
    let action = form.action;
    let method = "DELETE";
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
      url: action,
      type: method,
      data: JSON.stringify({
        id_registro: form.elements[0].value,
      }),
      dataType: "json",
      success: function (info) {
        userinfo = info;
        $("#alertPrimarySystem").html(`Registro borrado!`).fadeIn();
        setTimeout(function () {
          $("#alertPrimarySystem").fadeOut();
        }, 2000);
        runAllBeforeUpdate();
      },
      error: function (jqXHR, status, error) {
        $("#alertDangerSystem")
          .html(
            `Registro no borrado, por favor informe a la administración el problema`
          )
          .fadeIn();
        setTimeout(function () {
          $("#alertDangerSystem").fadeOut();
        }, 2000);
        console.log(`Estado: ${status}`);
        console.log(`Error: ${error}`);
      },
      complete: function (jqXHR, status) {
        console.log(`Petición completada con estado: ${status}`);
      },
      timeout: 10000,
    });
  }
}

// Add register event !

$("#btnSaveRegistercpa").click(() => {
  if ($("#selectorOpcionesCustomers").val() == 0) {
    $("#alertDangerSystem").html(`Selecciona un cliente!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  } else if ($("#IARquantity").val() == 0) {
    $("#alertDangerSystem").html(`Agrega un volumen de venta!`).fadeIn();
    setTimeout(function () {
      $("#alertDangerSystem").fadeOut();
    }, 2000);
    return false;
  }
  let action = $("#BoxAddReg form").attr("action");
  let method = $("#BoxAddReg form").attr("method");
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
    url: action,
    type: method,
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
      userinfo = info;
      $("#alertPrimarySystem").html(`Registro guardado!`).fadeIn();
      setTimeout(function () {
        $("#alertPrimarySystem").fadeOut();
      }, 2000);

      runAllBeforeUpdate();
    },
    error: function (jqXHR, status, error) {
      $("#alertDangerSystem")
        .html(
          `Registro no guardado, por favor informe a la administración el problema`
        )
        .fadeIn();
      setTimeout(function () {
        $("#alertDangerSystem").fadeOut();
      }, 2000);
      console.log(`Estado: ${status}`);
      console.log(`Error: ${error}`);
    },
    complete: function (jqXHR, status) {
      console.log(`Petición completada con estado: ${status}`);
    },
    timeout: 10000,
  });
});

// it's updating the data every 10 seconds
// setInterval(() => {
//   $.ajax({
//     beforeSend: function (xhr, settings) {
//       // if (
//       //   !/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) &&
//       //   !this.crossDomain
//       // ) {
//       //   xhr.setRequestHeader("X-CSRFToken", csrf_token);
//       // }
//       console.clear();
//       console.log("Consultado...");
//     },
//     url: "/apirf",
//     type: "GET",
//     dataType: "json",
//     success: function (info) {
//       userinfo = info;
//       runAllBeforeUpdate();
//     },
//     error: function (jqXHR, status, error) {
//       console.log(`Estado: ${status}`);
//       console.log(`Error: ${error}`);
//     },
//     complete: function (jqXHR, status) {
//       console.log(`Petición completada con estado: ${status}`);
//     },
//     timeout: 4500,
//   });
// }, 5000);

// manage when the user press enter
$("#IARquantity").on("keydown", function (e) {
  if (e.which == 13) {
    $("#btnSaveRegistercpa").click();
  }
});
