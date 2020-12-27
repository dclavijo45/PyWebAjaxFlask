// insert data to view

// clientes box
let clientesAlcanzados = [];
for (let i = 0; i <= userinfo.reports.id_customer.length; i++) {
  //console.log(i);
  for (let j = 0; j < userinfo.customers.id.length; j++) {
    if (
      userinfo.reports.id_customer[i] == userinfo.customers.id[j] &&
      clientesAlcanzados.includes(userinfo.reports.id_customer[i]) == false
    ) {
      clientesAlcanzados.push(userinfo.reports.id_customer[i]);
    }
  }
}

document.getElementById("qntCustomersAlcn").innerHTML =
  clientesAlcanzados.length;

document.getElementById("porcentajeCus1Alcn").innerHTML = `restante ${
  clientesAlcanzados.length
}/${userinfo.customers.total} - ${(
  (clientesAlcanzados.length * 100) /
  userinfo.customers.total
).toFixed(2)}%`;

// capital total box
let capitalTotalCus1 = 0;
for (let i = 0; i < userinfo.reports.precio_producto_vendido.length; i++) {
  capitalTotalCus1 += userinfo.reports.precio_producto_vendido[i];
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
//let cadena = capitalTotalCus1Format2.join("");

document.getElementById("capitalTotalCus1").innerHTML = "";

// chart info
function randomScalingFactor() {
  return Math.trunc(Math.random() * 5000);
}
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
  type: "line",
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
        label: "Semana pasada",
        borderColor: chartColors.orange,
        backgroundColor: chartColors.yellow,
        data: [
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
        ],
      },
      {
        label: "Semana actual",
        borderColor: chartColors.purple,
        backgroundColor: chartColors.blue,
        data: [
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
          randomScalingFactor(),
        ],
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
    },
    hover: {
      mode: "index",
    },
    scales: {
      xAxes: [
        {
          scaleLabel: {
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

// set date now cpAdmin input date
let dateNow = new Date();
let field = document.querySelector("#datenow");
field.value =
  dateNow.getFullYear().toString() +
  "-" +
  (dateNow.getMonth() + 1).toString().padStart(2, 0) +
  "-" +
  dateNow.getDate().toString().padStart(2, 0);

// setup input price product as not change
$("#InputPricecpa").change(function (e) {
  e.preventDefault();
});
$("#InputPricecpa").keydown(function (e) {
  e.preventDefault();
});

//set btn to events add register
$("#btnSaveRegistercpa").click(function (e) {
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
