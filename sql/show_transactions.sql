select
   t.id,
   date_format(t.trans_date, '%m/%d/%Y') as trans_date,
   t.type,
   c.name as contact,
   o.name as owner,
   concat_ws(', ', o.city, o.state) as location,
   p.id as piece_id,
   concat_ws('-', p.name, p.version) as piece,
   -- price,
   -- commision,
   -- concat(
   --   round(((price-total)/total) * 100, 2),
   --    '%') as commision_perc,
   total
   
from
   trans t
   join pieces p on t.piece_id = p.id
   join contacts c on t.contact_id = c.id
   join contacts o on t.owner_id = o.id

order by
   t.trans_date desc
;
