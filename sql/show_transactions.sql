set @total := 0;

select
   t.created as trans_date,
   c.fullname as contact,
   o.fullname as owner,
   p.name as piece,
   t.sale_price,
   coalesce(t.credit, '') as credit,
   coalesce(t.debit, '') as debit,
   (@total := @total + coalesce(t.credit, 0) - coalesce(t.debit, 0)) as total

from
   transactions t
   left join contacts c on t.contact_id = c.id
   left join contacts o on t.owner_id = o.id
   left join pieces p on t.piece_id = p.id

order by
   t.created
;
