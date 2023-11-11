create table trans (
  id           integer unsigned not null auto_increment primary key,
  trans_date   date not null,
  type         enum('sale', 'gift', 'donation', 'not for sale',
                    'no longer exists', 'lost') not null,
  contact_id   integer unsigned not null,
  owner_id     integer unsigned,
  piece_id     integer unsigned not null,
  edition      integer unsigned not null default 1,
  price        decimal(9,2),
  commision    decimal(9,2),
  total        decimal(9,2),
  notes        varchar(255),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,

  unique key(piece_id, edition),

  constraint t_contact_id foreign key (owner_id) references contacts(id),
  constraint t_owner_id foreign key (owner_id) references contacts(id),
  constraint t_piece_id foreign key (piece_id) references pieces(id)
)
engine InnoDB default charset=utf8;
;

create trigger trans_create before insert on trans
   for each row set new.r_created = now()
;
