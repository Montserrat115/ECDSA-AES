--- Base de Datos Gimnasio  ---

-- Solo si usas SQLite o si puedes cambiar la estructura
create table cliente(
   cedula INTEGER PRIMARY KEY AUTOINCREMENT,
   nombre varchar(30) not null,
   apellido_1 varchar(30) not null,
   apellido_2 varchar(30) not null,
   direccion varchar(50) default 'N/A',
   e_mail varchar(30) default '*@*.com',
   fecha_inscripcion date not null,
   celular int not null,
   huella_biometrica varbinary(512) not null,
   tarjeta_ultimos4 char(4),
   tarjeta_token varchar(100),
   foto_url varchar(255)
);


create table instructores(
    cod_instructor int not null,
    nombre varchar(30) not null,
    apellido_1 varchar(30) not null,
    apellido_2 varchar(30) not null,
    direccion varchar(50),
    e_mail varchar(30),
    tel_cel int not null,
    fecha_contratacion date not null,
    constraint pkinstructores primary key (cod_instructor)
);

create table pagoMensualidad(
    cod_venta int not null,
    cedula_cliente int not null,
    fecha_venta date not null,
    valor_venta decimal(10,2) not null,
    constraint pkventas primary key (cod_venta),
    constraint fkventas_cliente foreign key (cedula_cliente) references cliente (cedula)
);

create table ventasInstructores(
    cod_venta int not null,
    cod_instructor int not null,
    valor_venta decimal(10,2) not null,
    constraint pkventasI primary key (cod_venta),
    constraint fkventasI_instructor foreign key (cod_instructor) references instructores (cod_instructor)
);

--c. Agregar a la tabla cliente los campos: Celular int not null 
alter table cliente add celular int not null;


/*e. Validar en las tablas Cliente e Instructores que si el campo e-mail no tiene datos se debe
almacenar lo siguiente *@*.com y si el campo direcci?n de ambas tablas no tiene datos
se debe almacenar N/A.*/
alter table cliente modify direccion default 'n/a';
alter table instructores modify direccion default 'n/a';

alter table cliente modify e_mail default '*@*.com';

alter table instructores modify e_mail  default '*@*.com';


/*f. Establecer los campos Cedula_Cliente, Cod_Instructor , Cod_Maquina , como llaves
for?neas en la tabla Rutinas.*/
alter table rutinas add constraint fkrutina_cliente foreign key (cliente) references cliente (cedula);
alter table rutinas add constraint fk2rutina_instructor foreign key (instructor) references instructores (cod_instructor);

-- Para almacenar la plantilla biométrica (en forma de cadena base64 o binaria cifrada)
alter table cliente add huella_biometrica varbinary(512) not null;

-- Para almacenar los datos de tarjeta (sólo los últimos 4 dígitos y un token o alias si aplica)
alter table cliente add tarjeta_ultimos4 char(4);
alter table cliente add tarjeta_token varchar(100);
alter table cliente add foto_url varchar(255);
