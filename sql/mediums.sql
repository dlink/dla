create table mediums (
  id           integer unsigned not null auto_increment primary key,
  code         varchar(20)      not null,
  name         varchar(255)     not null,
  r_created    datetime         null,
  r_updated    timestamp        not null
    default current_timestamp on update current_timestamp,

  unique key(code)
)
engine InnoDB default charset=utf8;
;

create trigger mediums_create before insert on mediums
   for each row set new.r_created = now()
;
insert into mediums (code, name) values ('sculpt', 'Sculpture');
insert into mediums (code, name) values ('paint', 'Painting');
insert into mediums (code, name) values ('draw', 'Drawing');
insert into mediums (code, name) values ('shirt', 'T-Shirt');

select * from mediums;
