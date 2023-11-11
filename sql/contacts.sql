create table contacts (
   id           integer unsigned not null auto_increment primary key,
   first_name   varchar(255),
   middle_name  varchar(255),
   last_name    varchar(255),
   fullname     varchar(255),
   company_name varchar(255),
   name         varchar(255),
   email        varchar(255),
   website      varchar(255),
   notes        varchar(255),
   address1     varchar(190),
   address2     varchar(50),
   city         varchar(35),
   state        varchar(35),
   zipcode      varchar(15),
   country      varchar(15) default 'USA',
   authorized   boolean not null default 0,  -- authorized to use their name

   r_created   datetime,
   r_updated   timestamp not null
     default current_timestamp on update current_timestamp,

   unique key (email)

) engine=innodb default charset=utf8
;

create trigger contacts_create before insert on contacts
   for each row set new.r_created = now()
;

create trigger contacts_insert_fullname before insert on contacts
   for each row
      set new.fullname =
         concat_ws(' ',
	    new.first_name,
            nullif(new.middle_name, ''),
            new.last_name)
;

create trigger contacts_update_fullname before update on contacts
   for each row
      set new.fullname =
         concat_ws(' ',
	    new.first_name,
            nullif(new.middle_name, ''),
            new.last_name)
;

create trigger contacts_insert_name before insert on contacts
   for each row
      set new.name = if(new.company_name is not null,
                        new.company_name,
                        concat_ws(' ',
	                   new.first_name,
                           nullif(new.middle_name, ''),
                           new.last_name)
			);
;
create trigger contacts_update_name before update on contacts
   for each row
      set new.name = if(new.company_name is not null,
                        new.company_name,
                        concat_ws(' ',
	                   new.first_name,
                           nullif(new.middle_name, ''),
                           new.last_name)
			);
;
