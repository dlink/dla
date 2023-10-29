select
   s.id,
   date_format(s.sale_date, '%m/%d/%Y') as sale_date,
   c.name as contact,
   o.name as owner,
   concat_ws(', ', o.city, o.state) as location,
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

order by
   s.sale_date desc
;
