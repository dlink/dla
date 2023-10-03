alter table piece_images
   add column sort_order integer unsigned not null default 1 after filename
;
