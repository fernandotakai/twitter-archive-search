Twitter Archive Search
========

This a simple web interface for searching through your twitter archive with whoosh.
After installing the requirements, index your tweets using

    python index_tweets.py -p /path/to/your/archive/tweets/data/js/tweets/

Where path is your archive unzipped.

(Indexing takes ~5min with my ~120k tweets and uses 200mb of ram using cpython.)

After you index, you can run the webserver using python app.py (by default, it uses port 5000).
Some queries you can do:

* geo:yes date:2011 (all your tweets that have geolocalization from 2011)
* reply:yes sc2 (all your replies that are related to starcraft 2)


TODO
-------

* Endless scroll (for now you need to click on more to load more tweets)
* Use something like angular.js to make js more simple
* Support indexing directly from .zip archive
* Support to upload .zip directly through the web interface and index in the background


License
-------
BSD and that's it
