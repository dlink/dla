
create table piece_images (
   id          integer unsigned not null auto_increment primary key,
   piece_id    integer unsigned not null,
   filename    varchar(255)     not null,
   active      boolean          not null default 1,
   
   r_created   datetime         null,
   r_updated   timestamp        not null 
      default current_timestamp on update current_timestamp,

   constraint pi_piece_id foreign key (piece_id) references pieces (id)
) 
engine InnoDB default charset=utf8;
;

create trigger piece_images_create before insert on piece_images
   for each row set new.r_created = now()
;
