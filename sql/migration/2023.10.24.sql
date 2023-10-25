alter table pieces
   add column show_in_gallery integer unsigned not null default 1
      after weight_uom
;
