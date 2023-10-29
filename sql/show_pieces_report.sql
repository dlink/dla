
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
      ), '') as dim

from
   pieces p
   join mediums m on p.medium_id = m.id

order by
   p.created_year desc
