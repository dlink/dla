select
   t.id,
   t.created,
   tt.name as type,
   coalesce(c.company_name, c.fullname) as contact,
   coalesce(o.company_name, o.fullname) as owner,
   concat_ws('-', p.name, p.edition) as piece,
   coalesce(t.sale_price, '') as sale_price,
   coalesce(t.credit, '') as credit,
   coalesce(t.debit, '') as debit

from
   transactions t
   join transaction_types tt on t.type_id = tt.id
   join contacts c on t.contact_id = c.id
   join contacts o on t.owner_id = o.id
   join pieces p on t.piece_id = p.id
;
