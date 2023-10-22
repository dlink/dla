create table pieces (
  id           integer unsigned not null auto_increment primary key,  
  medium_id    integer unsigned not null,
  code         varchar(100) not null,
  name         varchar(100) not null,
  edition      integer unsigned not null default 1,
  sort_order   integer unsigned not null default 1,
  status_id    integer unsigned not null default 0,
  owner_id     integer unsigned,
  material     varchar(100),
  created      datetime,
  created_year integer unsigned,
  length       decimal(6,2),
  width        decimal(6,2),
  height       decimal(6,2),
  dim_uom      varchar(5),
  weight       decimal(6,2),
  weight_uom   varchar(5),
  location     varchar(250),
  short_description varchar(250),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,
 
  unique key (code, edition),
  constraint p_status_id foreign key (status_id) references piece_statuses(id),
  constraint p_owner_id foreign key (owner_id) references contacts(id)
)
engine InnoDB default charset=utf8;
;

create trigger pieces_create before insert on pieces
   for each row set new.r_created = now()
;
