create table collectors (
   id          integer unsigned not null auto_increment primary key,
   first_name  varchar(255),
   middle_name varchar(255),
   last_name   varchar(255),
   email       varchar(255),
   address1    varchar(190),
   address2    varchar(50),
   city        varchar(35),
   state       varchar(35),
   zipcode     varchar(15),
   country     varchar(15),

   r_created   datetime,
   r_updated   timestamp not null
     default current_timestamp on update current_timestamp,

   unique key (email)

) engine=innodb default charset=utf8
;

create trigger collectors_create before insert on collectors
   for each row set new.r_created = now()
;
