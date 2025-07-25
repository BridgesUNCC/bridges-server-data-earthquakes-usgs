# Routes

only provide 3 routes:

1. Route `/` returns only documentation (if any)
2. Route `/eq/latest/<int:number>` returns the latest number earthquakes.
3. Route `/eq` returns all the earthquakes there is to return.

## JSON

the earthquakes are returned in a JSON as `JSON['Earthquakes']` which is an array. Each earthquake has:

- `eq['id']` the id of the quake assigned by USGS
- `eq['geometry']['coordinates']` an array of lat, long, depth
- `eq['url']` that points to more info from the usgs
- `eq['properties']['mag']` the magnitude in Richter Local scale
- `eq['properties']['place']` a text description of the location
- `eq['properties']['title']` a text description of the quake
- `eq['properties']['time']` a UNIX timestamp when the quake happened



