select
   s.id,
   s.sale_date,
   c.name as contact,
   o.name as owner,
   concat_ws('-', p.name, p.version) as piece,
   sale_price,
   commision,
   concat(
      round(((sale_price-total)/total) * 100, 2),
      '%') as commision_perc,
   total
   
from
   sales s
   join pieces p on s.piece_id = p.id
   join contacts c on s.contact_id = c.id
   join contacts o on s.owner_id = o.id
;
