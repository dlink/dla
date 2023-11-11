alter table pieces
   add column duplicate_id integer unsigned
   after orig_piece_id
;

alter table pieces
   add constraint p_duplicate_id foreign key (duplicate_id)
      references pieces(id)
;

alter table trans
    add column notes varchar(255) after total
;

alter table contacts
    add column notes varchar(255) after website
;

alter table pieces
    add column notes varchar(255) after show_in_gallery
;

alter table trans
    change column type
       type enum('sale', 'gift', 'donation', 'no longer exists') not null
;
alter table trans
    change column type
    type enum('sale', 'gift', 'donation', 'not for sale',
              'no longer exists') not null
;
