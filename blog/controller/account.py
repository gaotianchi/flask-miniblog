from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from blog.model.database import User

account = Blueprint("account", __name__)


@account.before_app_request
def load_user():
    g.current_user = None
    userid = session.get("userid")
    if userid:
        user = User.query.get(int(userid))
        if user:
            g.current_user = user

    if request.endpoint:
        if request.endpoint.startswith("author"):
            if not g.current_user:
                flash("Please log in.")
                return redirect(url_for("account.sign_in", next=request.url))
    return None


@account.route("/sign/up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        User.create(username, password)
        flash(f"Successfully create account {username}, please log in.")
        return redirect(url_for("account.sign_in"))
    return render_template("account/sign-up.html")


@account.route("/sign/in", methods=["GET", "POST"])
def sign_in():
    userid = session.get("userid")
    next = request.args.get("next")
    if userid:
        user = User.query.get_or_404(int(userid))
        if next:
            flash(f"Log in successfully. Welcome {user.username}")
            return redirect(next)

        return redirect(url_for("visitor.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Wrong username!")
            return redirect(url_for("account.sign_in"))
        if not user.validate_password(password):
            flash("Wrong password!")
            return redirect(url_for("account.sign_in"))

        session["userid"] = user.id
        flash(f"Log in successfully. Welcome {user.username}")
        if next:
            return redirect(next)
        return redirect(url_for("visitor.index"))

    return render_template("account/sign-in.html")


@account.route("/log/out", methods=["GET"])
def log_out():
    userid = session.get("userid")
    if userid:
        session["userid"] = None
    flash("Log out.")
    return redirect(url_for(".sign_in"))
