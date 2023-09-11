drop table if exists mediums;

create table mediums (
  id          serial primary key,
  code        varchar(20) not null,
  name        varchar(100) not null,
  r_created   timestamptz default current_timestamp,
  r_updated   timestamptz,

  unique(code)
);
create trigger mediums_updates
   before insert or update on mediums
      for each row
         execute function set_created_and_updated()
;
insert into mediums (code, name) values ('sculpt', 'Sculpture');
insert into mediums (code, name) values ('paint', 'Painting');
insert into mediums (code, name) values ('draw', 'Drawing');
insert into mediums (code, name) values ('shirt', 'T-Shirt');
insert into mediums (code, name) values ('shirt', 'T-Shirt');
