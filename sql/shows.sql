
create table shows (
   id            integer unsigned not null auto_increment primary key,
   code          varchar(35)      not null,
   name          varchar(255)     not null,
   description   text             ,
   contact_id    integer unsigned ,
   active        boolean          not null,
   start_date    date,
   end_date      date,
   opening       date,

   r_created     datetime         null,
   r_updated     timestamp        not null
	default current_timestamp on update current_timestamp,

   unique key(code),
   unique key(name)

) engine InnoDB default charset=utf8;
;

create trigger shows_create before insert on shows
   for each row set new.r_created = now()
;
