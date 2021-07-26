drop table if exists tasks;
drop table if exists task_status;
drop table if exists users;

create table task_status(
    id serial primary key,
    name text,
    status boolean
);

insert into task_status(name,status) values ('Yet to Start',FALSE);
insert into task_status(name,status) values ('in progress',FALSE);
insert into task_status(name,status) values ('Completed',FALSE);

create table users(
    id serial primary key,
    username text,
    pass varchar(20)
);

create table tasks(
    id serial primary key,
    user_id int,
    task_name text,
    added_on date,
    due_datetime datetime,
    status serial references task_status(id)
);
