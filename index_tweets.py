import sys
import os.path
import argparse
import simplejson

from whoosh.index import create_in
from whoosh.index import open_dir

from dateutil.parser import parse
from datetime import datetime
from search_index import TweetSchema

clean = lambda it: simplejson.loads("".join(it[1:]).replace("\n", ""))

def index_json(json, writer):
    for tweet in json:
        latitude, longitude = tweet['geo'].get('coordinates', [0, 0])
        has_geo = bool(latitude and longitude)
        is_reply = bool(tweet.get('in_reply_to_status_id', ''))
        url = u"http://twitter.com/%s/status/%s" % (tweet['id'], tweet['user']['screen_name'])

        if not isinstance(tweet['text'], unicode):
            tweet['text'] = unicode(tweet['text'])

        writer.add_document(
            id=unicode(tweet['id_str']),
            url=url,
            text=tweet['text'],
            source=unicode(tweet['source']),
            reply=is_reply,
            in_reply_to_id=unicode(tweet.get('in_reply_to_status_id', '')),
            in_reply_to_name=unicode(tweet.get('in_reply_to_screen_name')),
            user_mentions=u' '.join([u['screen_name'] for u in tweet['entities']['user_mentions']]),
            hashtags=u' '.join([u['text'] for u in tweet['entities']['hashtags']]),
            urls=u' '.join([u['expanded_url'] for u in tweet['entities']['urls']]),
            geo=has_geo,
            latitude=latitude,
            longitude=longitude,
            date=parse(tweet['created_at'])
        )

    print "Indexed %s tweets" % len(json)

def open_index():
    if not os.path.exists("index"):
        os.mkdir("index")
        ix = create_in("index", TweetSchema)
    else:
        ix = open_dir("index")

    return ix.writer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Indexes your tweets using whoosh')
    parser.add_argument('-p', '--path', required=True,
                        help="Path to your tweets. From your archive, it's 'data/js/tweets/'")

    args = parser.parse_args()
    path = os.path.expanduser(args.path)

    if not os.path.exists(path):
        print "Path %s does not exist" % path
        sys.exit(1)

    if not os.path.isdir(path):
        print "Path %s is not a directory" % path
        sys.exit(1)

    files = [f for f in os.listdir(path) if ".js" in f]

    if not files:
        print "Could not find any .js files at %s" % path
        sys.exit(1)

    started = datetime.now()
    print "Started %s" % started

    index_writer = open_index()

    for file in files:
        json_path = os.path.join(path, file)
        print "Reading %s" % file

        with open(json_path) as f:
            json = clean(f.readlines())
            index_json(json, index_writer)
            json = None

    index_writer.commit()

    finished = datetime.now()
    print "Finished, took %s" % (finished - started)
