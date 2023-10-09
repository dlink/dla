create table users (
  id          integer unsigned  not null,
  username    varchar(255)      not null,
  first_name  varchar(255)      , 
  last_name   varchar(255)      not null, 
  email       varchar(255)      not null,
  -- role_id     integer unsigned  not null default 1,
  active      integer unsigned  not null default 1,

  r_created   datetime          not null,
  r_updated   timestamp         not null 
     default current_timestamp on update current_timestamp

  -- constraint user_role_id foreign key (role_id) references roles (id)
) 
engine InnoDB default charset=utf8;
;

create trigger users_create before insert on users
   for each row set new.r_created = now()
;

insert into users
   (id, username, first_name, last_name, email, active)
values
   (1, 'dlink', 'David', 'Link', 'dvlink@gmail.com', 1)
;

select * from users;
