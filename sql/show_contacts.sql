select
   c.id,
   c.fullname,
   coalesce(c.company_name, '') as company_name,
   coalesce(c.email, '') as email,
   case
      when c.city is not null and c.state is not null then 
         concat_ws(', ', c.city, c.state)
      when c.state is not null then
         c.state
      else
         ''
      end as location
   
from
   contacts c
;
