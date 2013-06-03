from whoosh import fields

class TweetSchema(fields.SchemaClass):
    id = fields.ID(stored=True, unique=True)
    url = fields.ID(stored=True, unique=True)

    text = fields.TEXT(stored=True)
    source = fields.TEXT(stored=True)

    reply = fields.BOOLEAN(stored=True)
    in_reply_to_id = fields.TEXT(stored=True)
    in_reply_to_name = fields.TEXT(stored=True)

    user_mentions = fields.KEYWORD(stored=True)
    hashtags = fields.KEYWORD(stored=True)
    urls = fields.KEYWORD(stored=True)

    geo = fields.BOOLEAN(stored=True)
    latitude = fields.NUMERIC(stored=True)
    longitude = fields.NUMERIC(stored=True)

    date = fields.DATETIME(stored=True)

