from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from blog.model.database import Category, Post, Visitor
from blog.utlis import calculate_the_number_of_reads_per_article, count_monthly_visitor

author = Blueprint("author", __name__)


@author.route("/add/post", methods=["POST", "GET"])
def add_post():
    if request.method == "POST":
        form = request.form
        title = form.get("posttitle")
        body = form.get("postbody")
        category_id = form.get("postcategory", type=int)

        category = Category.query.get(category_id)

        new_post = Post.create(title=title, body=body, category=category)

        return redirect(url_for("visitor.read_post", post_id=new_post.id))

    categories = Category.query.all()

    return render_template("author/add-post.html", categories=categories)


@author.route("/update/post/<post_id>", methods=["GET", "POST"])
def update_post(post_id):
    post = Post.query.get(post_id)
    categories = Category.query.all()
    if not post:
        return jsonify("No post was found!"), 404

    if request.method == "POST":
        form = request.form
        title = form.get("posttitle")
        body = form.get("postbody")
        category_id = form.get("postcategory", type=int)

        category = Category.query.get(category_id)

        new_post = post.update(title=title, body=body, category=category)
        url = url_for("visitor.read_post", post_id=new_post.id)
        print(url)

        return redirect(url_for("visitor.read_post", post_id=new_post.id))

    return render_template("author/edit-post.html", post=post, categories=categories)


@author.route("/manage-index", methods=["GET"])
def manage_index():
    return render_template("author/manage-index.html")


@author.route("/get/visitors", methods=["GET"])
def get_visitor_data():
    classification_method = request.args.get("classification_method")
    match classification_method:
        case "month":
            timestamps = Visitor.query.with_entities(Visitor.timestamp).all()
            monthly_visitor = count_monthly_visitor([t[0] for t in timestamps])
            return jsonify(monthly_visitor), 200
        case "article":
            posts = (
                Visitor.query.with_entities(Visitor.detail)
                .filter(Visitor.detail.isnot(None))
                .all()
            )

            result = calculate_the_number_of_reads_per_article([p[0] for p in posts])
            return jsonify(result[:10]), 200


@author.route("/manage/post", methods=["GET", "POST"])
def manage_post():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template("author/manage-post.html", posts=posts)


@author.route("/manage/category", methods=["GET", "POST"])
def manage_category():
    categories = Category.query.all()
    return render_template("author/manage-category.html", categories=categories)


@author.route("/delete/post/<post_id>", methods=["POST", "DELETE"])
def delete_post(post_id: int):
    post = Post.query.get(post_id)
    if not post:
        return jsonify("No post was found."), 404
    title = post.title
    post.delete()
    return jsonify(f"Successfully delete post {title}."), 200


@author.route("/update/category/<category_id>", methods=["GET", "POST"])
def update_category(category_id: int):
    category = Category.query.get(category_id)
    if not category:
        return jsonify("No category was found."), 404
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        category.update(title, body)

        return jsonify(f"Successfully update category {category.title}"), 200

    return render_template("author/edit-category.html", category=category)
