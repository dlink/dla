alter table pieces
   add column editions integer unsigned not null default 1
   after version
;

alter table trans
   add column edition integer unsigned not null default 1
   after piece_id
;

alter table trans
   drop key piece_id,
   add unique key(piece_id, edition)
;
