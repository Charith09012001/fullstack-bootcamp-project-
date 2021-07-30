drop table if exists tasks;
drop table if exists task_status;
drop table if exists users;

create table task_status(
    id serial primary key,
    name text,
    status boolean
);


insert into task_status(name,status) values ('in progress',FALSE);
insert into task_status(name,status) values ('Completed',FALSE);

create table users(
    id varchar(100) primary key,
    usermail varchar(50),
    username text ,
    pass varchar(20)
);

create table tasks(
    id serial primary key,
    user_id varchar(100) references users(id),
    task_name text,
    task_description text,
    added_on date,
    due_date date,
    due_time time,
    status serial references task_status(id)
    
);
