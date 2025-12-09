create database if not exists classfocus;
use classfocus;

create table if not exists user (
  id int not null auto_increment primary key,
  nome varchar(120),
  email varchar(120) not null unique,
  password_hash text not null
);

create table if not exists tarefa (
  id int not null auto_increment primary key,
  nome varchar(255) not null,
  data_hora datetime not null,
  disciplina varchar(120),
  user_id int default null,
  foreign key (user_id) references user(id)
);