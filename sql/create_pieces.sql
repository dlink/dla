create table pieces (
  id           integer unsigned not null auto_increment primary key,  
  medium_id    integer unsigned not null,
  code         varchar(20) not null,
  name         varchar(100) not null,
  description  varchar(250),
  material     varchar(100),
  created      datetime,
  created_year integer unsigned,
  length       decimal(6,2),
  width        decimal(6,2),
  height       decimal(6,2),
  dim_uom      varchar(5),
  weight       decimal(6,2),
  weight_uom   varchar(5),
  notes        varchar(250),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,
 
  unique key (code)
)
engine InnoDB default charset=utf8;
;

create trigger pieces_create before insert on pieces
   for each row set new.r_created = now()
;

insert into pieces
   (medium_id, code, name, material, created_year, length, width,
   height, dim_uom)
values
  (1, 'gardian', 'Guardian', 'Welded Aluminum, Powder Coated',
  '2023', 2, 2, 6, 'ft')
;

select * from pieces;
