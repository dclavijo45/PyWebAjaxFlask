$(function () {
  // Sidebar toggle behavior
  $("#sidebarCollapse").on("click", function () {
    $("#sidebar, #content").toggleClass("active");
  });
});

// userinfoOBJ
profile_image = document.getElementById("profile_image");
profile_imageV = document.getElementById("profile_imageV");
profile_image.src = `/static/img/profiles/${userinfo.profile_image}`;
profile_imageV.src = `/static/img/profiles/${userinfo.profile_image}`;

let nombre = userinfo.username;
if (nombre.indexOf(" ") == -1) {
  document.getElementById("DBNombre2").innerHTML = nombre.substring(-1, 8);
} else {
  document.getElementById("DBNombre2").innerHTML =
    nombre.substring(-1, 8) + ".";
}
