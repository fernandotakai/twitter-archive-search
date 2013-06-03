import datetime
import simplejson as json

from flask import Flask, request, render_template, Response

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser.dateparse import DateParserPlugin

from search_index import TweetSchema

app = Flask(__name__)

search_index = open_dir("index")
parser = QueryParser("text", TweetSchema())
parser.add_plugin(DateParserPlugin())

class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def jsonify(**data):
    return Response(json.dumps(data, cls=APIEncoder), mimetype='application/json')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    q = request.args.get("q", "")
    page = int(request.args.get("p", ""))

    with search_index.searcher() as searcher:
        query = parser.parse(q)
        try:
            results = searcher.search_page(query, page, sortedby="date", pagelen=25)
        except ValueError:
            return jsonify(results=[], finished=True)

        return jsonify(results=[dict(r) for r in results], finished=results.is_last_page())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
