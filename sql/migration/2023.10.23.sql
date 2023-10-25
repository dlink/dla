alter table pieces
   add column orig_piece_id integer unsigned after edition,
   add constraint p_orig_piece_id foreign key (orig_piece_id)
      references pieces(id)
;
