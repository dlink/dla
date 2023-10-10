
select
   p.id,
   p.created_year as created,
   m.name as medium,
   p.name as name,
   p.material,
   if(p.length,
      concat(
         concat_ws('x', round(p.length,0),
	                round(p.width,0),
			round(p.height,0)
		  ),
	 ' in.'
      ), '') as dim,
   s.name as status,
   o.fullname as owner,
   concat_ws(', ', o.city, o.state) as location

from
   pieces p
   join mediums m on p.medium_id = m.id
   join piece_statuses s on p.status_id = s.id
   left join contacts o on p.owner_id = o.id

order by
   p.created_year desc
