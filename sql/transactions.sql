create table transactions (
  id           integer unsigned not null auto_increment primary key,
  created      date,
  type_id      integer unsigned not null,
  contact_id   integer unsigned not null,
  owner_id     integer unsigned,
  piece_id     integer unsigned not null,
  sale_price   decimal(9,2),
  credit       decimal(9,2),
  debit        decimal(9,2),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,
 
  constraint t_type_id foreign key (type_id) references transaction_types(id),
  constraint t_contact_id foreign key (owner_id) references contacts(id),
  constraint t_owner_id foreign key (owner_id) references contacts(id)
)
engine InnoDB default charset=utf8;
;

create trigger transactions_create before insert on transactions
   for each row set new.r_created = now()
;
