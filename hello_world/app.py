import awsgi
from flask import Flask, jsonify, request

import feed_poller
import feed_repository
import item_repository
from feed import Feed

app = Flask(__name__)
feed_poller.start_polling()


@app.route("/feeds")
def get_all_feeds():
    feeds = feed_repository.get_all_feeds()
    return jsonify({"feeds": feeds})


@app.route("/feeds", methods=["POST"])
def create_feed():
    feed = Feed(**request.get_json())
    return jsonify(feed_repository.create_feed(feed)), 201


@app.route("/items")
def get_all_items():
    items = item_repository.get_all_items()
    return jsonify({"items": items})


@app.route("/reads/<string:item_id>", methods=["GET"])
def mark_read(item_id: str):
    item = item_repository.get_one_item(item_id)


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})
