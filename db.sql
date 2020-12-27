CREATE SCHEMA liveone;

USE liveone;

CREATE TABLE usuarios(
	id int PRIMARY KEY AUTO_INCREMENT,
    nombres varchar(50) not null,
    apellidos varchar(55) not null,
    tipo_identificacion char(2) not null,
    num_identificacion varchar(15) not null,
    correo varchar(150) null,
    foto_perfil varchar(100) not null default 'targetblank.png',
    rol_usuario tinyint(2) not null default 1,
    clave_usuario varchar(300) not null,
    estado_usuario tinyint(1) not null default 1
);

CREATE TABLE productos(
	id int PRIMARY KEY AUTO_INCREMENT,
    nombre_producto varchar(20) not null,
    descripcion_producto varchar(100) not null,
    imagen_producto varchar(100) not null default 'targetblank.png',
    precio_producto double not null default 0,
    cantidad_producto varchar(100) not null default 0,
    observaciones_producto varchar(150) not null default 'No hay observaciones',
    creador_producto int not null,
    fecha_creacion datetime not null default now(),
    fecha_actualizacion datetime null default now(),
    foreign key(creador_producto) references usuarios(id)
);

CREATE TABLE clientes(
	id int PRIMARY KEY AUTO_INCREMENT,
    nombres varchar(20) not null,
    apellidos varchar(20) not null,
    alias varchar(15),
    tipo_identificacion char(2) not null,
    num_identificacion varchar(15) not null,
    correo varchar(150) null,
    foto_perfil varchar(100) not null default 'targetblank.png',
    producto_asociado int not null,
    creador_cliente int not null,
	estado_cliente tinyint(1) not null default 1,
    foreign key(creador_cliente) references usuarios(id),
    foreign key(producto_asociado) references productos(id)
);

CREATE TABLE reportes(
    id int PRIMARY KEY AUTO_INCREMENT,
    usuario_reportado int not null,
    usuario_reportador int not null,
    id_producto int not null,
    cantidad_venta double not null default 0,
    observacion_venta varchar(100) not null default 'No hay observaciones',
    fecha_creacion datetime not null default now(),
    fecha_actualizacion datetime null default now(),
    foreign key(usuario_reportador) references usuarios(id),
    foreign key(usuario_reportado) references clientes(id),
    foreign key(id_producto) references productos(id)
);

/*
SELECT * from reportes 
where ( ( month(fecha_actualizacion) = month(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY))
 and
 (day(fecha_actualizacion) >= day(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY)) and 
 day(fecha_actualizacion) <= (day(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY)) + 6) )  
 and
 year(fecha_actualizacion) = year(DATE_ADD(CURDATE(), INTERVAL - WEEKDAY(CURDATE()) DAY))) ) and usuario_reportador = 1;
*/