drop table if exists pieces;

create table pieces (
  id          serial primary key,
  medium_id   integer not null,
  code        varchar(20) not null,
  name        varchar(100) not null,
  description varchar(250),
  material    varchar(100),
  created     timestamptz,
  created_year integer,
  length      integer,
  width       integer,
  height      integer,
  dim_uom     varchar(5),
  weight      integer,
  weight_uom  varchar(5),
  notes       varchar(250),
  r_created   timestamptz default current_timestamp,
  r_updated   timestamptz not null,

  unique(code)
);

alter table pieces add constraint fk_medium_id
   foreign key (medium_id) references mediums (id)
;

create trigger pieces_set_created_and_updated
   before insert or update on pieces
      for each row
         execute function set_created_and_updated()
;

insert into pieces
   (medium_id, code, name, material, created_year, length, width, height, dim_uom)
values
  (1, 'gardian', 'Guardian', 'Welded Aluminum, Powder Coated', '2023', 2, 2, 6, 'ft');

select * from pieces;
