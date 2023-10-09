
create table piece_statuses (
   id            integer unsigned not null primary key,
   code          varchar(35)      not null,
   name          varchar(255)     not null,
   description   varchar(255)     ,
   active        boolean          not null,
   
   created       datetime         not null,
   updated       timestamp        not null 
        default current_timestamp on update current_timestamp,

   unique key(code),
   unique key(name)

) engine InnoDB default charset=utf8;
;

create trigger piece_statuses_create before insert
   on piece_statuses
   for each row set new.created = now()
;
