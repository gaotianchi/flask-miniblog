import re
from datetime import datetime, timedelta

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from blog.model.database import Category, Post, User, Visitor

visitor = Blueprint("visitor", __name__)


@visitor.before_request
def before_visitor():
    ip = request.remote_addr
    path = request.path
    three_minutes_ago = datetime.utcnow() - timedelta(minutes=3)
    v_query = Visitor.query.filter(
        Visitor.ip == ip, Visitor.timestamp >= three_minutes_ago
    ).order_by(Visitor.timestamp.desc())

    latest_v = v_query.first()
    if latest_v:
        if latest_v.banned:
            return (
                jsonify(
                    "You have been banned as your access frequency exceeds the maximum limit."
                ),
                403,
            )

    frequency = v_query.count() // 3
    if frequency > current_app.config["MAXIMUM_ACCESS_FREQUENCY"]:
        Visitor.create(ip=ip, url=path, banned=True)
        return jsonify("Your access frequency exceeds the maximum limit."), 403
    match request.endpoint:
        case "visitor.read_post":
            page_type = "post"
            detail = None
            if re.match(r"/read/post/(\d+)", request.path):
                post_id = int(re.match(r"/read/post/(\d+)", request.path).group(1))
                post = Post.query.get(post_id)
                detail = post.title
        case _:
            page_type = None
            detail = None

    Visitor.create(
        ip=request.remote_addr,
        url=request.path,
        page_type=page_type,
        detail=detail,
    )
    return None


@visitor.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@visitor.route("/read/post/<post_id>", methods=["GET"])
def read_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify("No post was found."), 404

    return render_template("visitor/read-post.html", post=post)


@visitor.route("/archive/post", methods=["GET"])
def archive_post():
    query = Post.query

    category_name = request.args.get("category")
    if category_name:
        category = Category.query.filter_by(title=category_name).first()
        if category:
            query = query.filter_by(category=category)

    posts = query.all()

    return render_template("visitor/archive-post.html", posts=posts)
