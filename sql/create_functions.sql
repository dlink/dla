-- set r_created on inserts
-- set r_updated on all updates

drop function if exists set_created_and_updated cascade;

create or replace function set_created_and_updated()
returns trigger as $$
begin
  if tg_op = 'INSERT' then
    new.r_created = now();
  end if;
  new.r_updated = now();
  return new;
end;
$$ language plpgsql
;
