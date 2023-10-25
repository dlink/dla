alter table pieces
   drop index code
;
alter table pieces
   change column edition version integer unsigned not null default 1
;
alter table pieces
   add unique key (code, version)
;
