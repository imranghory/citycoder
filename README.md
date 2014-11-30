citycoder 0.1
=============

Geocoder to convert free-form location strings to structured data. Focused on city level and higher (region/state/country) and runs locally.

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


##### Licence

Citycoder code is licenced under the MIT Licence; city data under CC-BY.

Copyright (c) 2014 Imran Ghory

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The cities15000.txt file is under CC-BY licence from Geonames.

