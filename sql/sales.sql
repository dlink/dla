create table sales (
  id           integer unsigned not null auto_increment primary key,
  sale_date    date,
  contact_id   integer unsigned not null,
  owner_id     integer unsigned,
  piece_id     integer unsigned not null,
  sale_price   decimal(9,2),
  commision    decimal(9,2),
  total        decimal(9,2),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,
 
  constraint s_contact_id foreign key (owner_id) references contacts(id),
  constraint s_owner_id foreign key (owner_id) references contacts(id)
)
engine InnoDB default charset=utf8;
;

create trigger sales_create before insert on sales
   for each row set new.r_created = now()
;
