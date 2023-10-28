select
   s.sale_date,
   concat_ws(', ', o.city, o.state) as city,
   concat_ws('-', p.name, p.version) as piece

from
   sales s
   join pieces p on s.piece_id = p.id
   join contacts o on s.owner_id = o.id
;
