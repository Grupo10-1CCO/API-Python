drop database samp;

create DATABASE SAMP;

USE SAMP;

CREATE TABLE Empresa(
	idEmpresa INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR (100),
    email VARCHAR (100),
    cnpj CHAR(14)
);

CREATE TABLE Usuario(
	idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR (100),
    email VARCHAR (100),
    senha VARCHAR (100),
    fkEmpresa INT,
    FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE Maquina(
	idMaquina INT PRIMARY KEY AUTO_INCREMENT,
	serialMaquina CHAR(12),
    nome VARCHAR(100),
    fkEmpresa INT,
    FOREIGN KEY (fkEmpresa) REFERENCES Empresa(idEmpresa)
);

CREATE TABLE Medida(
	idMedida INT PRIMARY KEY AUTO_INCREMENT,
    unidadeMedida VARCHAR (8)
);

CREATE TABLE Metrica(
	idMetrica INT PRIMARY KEY AUTO_INCREMENT,
    capturaMin DOUBLE,
    capturaMax DOUBLE
);

CREATE TABLE Componente(
	idComponente INT PRIMARY KEY AUTO_INCREMENT,
    nomeComponente VARCHAR (50),
    fkMaquina INT,
    fkMetrica INT,
    fkMedida INT,
    FOREIGN KEY (fkMaquina) REFERENCES Maquina (idMaquina),
    FOREIGN KEY (fkMetrica) REFERENCES Metrica (idMetrica),
    FOREIGN KEY (fkMedida) REFERENCES Medida (idMedida)
);

CREATE TABLE registro(
	idRegistro INT PRIMARY KEY AUTO_INCREMENT,
    momento DATETIME,
    captura DOUBLE,
    fkComponente INT,
    FOREIGN KEY (fkComponente) REFERENCES Componente (idComponente)
);
insert into empresa values(null, 'abc', 'abc@gmail', '12345678912345');
insert into medida values(NULL, '%'), (NULL, 'Ghz'), (NULL, 'Gb');

/*insert into empresa values(null, 'abc', 'sees', '12345678912345');
select idEmpresa from empresa where idEmpresa = 1;
select * from usuario;
select * from empresa;
select * from medida;
select * from maquina;
select * from componente;
select * from registro;
select * from componente;

insert into usuario values (null, 'joao', 'joao', MD5('123'), 1);
delete from maquina where idMaquina >= 0;
delete from componente where idComponente >= 0;
select * from usuario where email = 'teste' and senha = '202cb962ac59075b964b07152d234b70';
INSERT INTO registro VALUES(NULL, '2022-10-03 13:49:16.811754', 10.0, (select idComponente from componente where nomeComponente = 'RAM' and fkMaquina = 3)), 
(NULL, '2022-10-03 13:49:16.811754', 40.6, (select idComponente from componente where nomeComponente = 'RAM' and fkMaquina = 3)), (NULL, '2022-10-03 13:49:16.811754', 50.5, 
(select idComponente from componente where nomeComponente = 'Disco C:\\' and fkMaquina = 3));*/
