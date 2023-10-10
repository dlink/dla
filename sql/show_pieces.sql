create table show_pieces (
  id           integer unsigned not null auto_increment primary key,
  show_id      integer unsigned not null,
  piece_id     integer unsigned not null,

  r_created    datetime     null,
  r_updated    timestamp    not null
    default current_timestamp on update current_timestamp,

  unique key (show_id, piece_id),
  constraint sp_show_id foreign key (show_id) references shows(id),
  constraint sp_piece_id foreign key (piece_id) references pieces(id)
)
engine InnoDB default charset=utf8;
;

create trigger show_pieces_create before insert on show_pieces
   for each row set new.r_created = now()
;
