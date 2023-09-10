create table pieces (
  id          serial primary key
  mediums_id  integer not null,
  code        varchar(20) not null,
  name        varchar(100) not null,
  description varchar(250),
  material    varchar(100),
  created     timestamptz not null,
  length      integer unsigned,
  width       integer unsigned,
  height      integer unsigned,
  dim_uom     varchar(5),
  weight      integer unsigned,
  weight_uom  varchar(5),
  notes       varchar(250),
  r_created   timestamptz not null,
  r_updated   timestamptz not null,

  unique key code (code),
  constraint mediums_id foreign key (mediums_id) references mediums (id),
);

-- alter table pieces add constraint fk_mediums_id
--    foreign key (mediums_id) references mediums (id)
-- ;

create trigger pieces_set_created_and_updated
   before insert or update on pieces
      for each row
         execute function set_created_and_updated()
;

