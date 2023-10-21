
create table transaction_types (
   id            integer unsigned not null primary key,
   code          varchar(35)      not null,
   name          varchar(255)     not null,
   description   varchar(255)     ,
   active        boolean          not null,
   
   r_created       datetime       null,
   r_updated       timestamp      null
        default current_timestamp on update current_timestamp,

   unique key(code),
   unique key(name)

) engine InnoDB default charset=utf8;
;

create trigger transaction_types_create before insert
   on transaction_types
   for each row set new.r_created = now()
;
