create table piece_descriptions (
  id           integer unsigned not null auto_increment primary key,
  piece_id     integer unsigned not null,
  description  text,
  notes        varchar(250),

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,

  unique key (piece_id)
)
engine InnoDB default charset=utf8;
;

create trigger piece_descriptions_create before insert on piece_descriptions
   for each row set new.r_created = now()
;
