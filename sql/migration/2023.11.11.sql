alter table pieces
   add column duplicate_id integer unsigned
   after orig_piece_id
;

alter table pieces
   add constraint p_duplicate_id foreign key (duplicate_id)
      references pieces(id)
;
