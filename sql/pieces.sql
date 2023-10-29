create table pieces (
  id           integer unsigned not null auto_increment primary key,  
  medium_id    integer unsigned not null,
  code         varchar(100) not null,
  name         varchar(100) not null,
  version      integer unsigned not null default 1,
  orig_piece_id integer unsigned,
  sort_order   integer unsigned not null default 1,
  material     varchar(100),
  created      datetime,
  created_year integer unsigned,
  length       decimal(6,2),
  width        decimal(6,2),
  height       decimal(6,2),
  dim_uom      varchar(5),
  weight       decimal(6,2),
  weight_uom   varchar(5),
  show_in_gallery  integer unsigned not null default 1,
  location     varchar(250),
  short_description varchar(250),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,
 
  unique key (code, version),
  constraint p_orig_piece_id foreign key (orig_piece_id) references pieces(id)
)
engine InnoDB default charset=utf8;
;

create trigger pieces_create before insert on pieces
   for each row set new.r_created = now()
;
