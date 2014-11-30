citycoder 0.1
=============

Geocoder to convert free-form location strings to structured data. Focused on city level and higher (region/state/country).

If you're dealing with user supplied location strings (for example from Twitter bios) and want to convert them into structured data (i.e extract country) then that's what citycoder will give you. It runs entirely locally so you don't need to rely on third-party geocoding services like geomind, etc.

It's largely heuristic based and tries to make similar judgements to how a human would decide what is meant. So for instance if just a city name is given and it's ambiguous it'll pick the largest city with that name (by population size).

Don't use it for anything where you have to be 100% correct.

##### Examples

```python
>>> parselocation('London')
{'Country': u'United Kingdom', 'Region': None, 'City': 'London'}
>>> parselocation('Boston, MA')
{'Country': u'United States', 'Region': 'Massachusetts', 'City': 'Boston'}
>>> parselocation('France')
{'Country': u'France', 'Region': None, 'City': None}
>>> parselocation('California')
{'Country': u'United States', 'Region': 'California', 'City': None}
```
