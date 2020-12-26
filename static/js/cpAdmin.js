// insert data to view
document.getElementById("qntCustomersAlcn").innerHTML =
  userinfo.customers.total;

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
