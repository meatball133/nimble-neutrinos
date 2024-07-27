from flask import request, render_template, session, redirect, url_for, abort
from src.webapp import db, discord_api


def mainpage():
    return render_template("index.j2")


def gallery():
    return render_template("gallery.j2")


def management():
    return render_template("management.j2")


def login():
    if session.get("user_id") is not None:
        return redirect(url_for("mainpage"))
    return redirect(discord_api.oauth_url)


def authorizer():
    code = request.args.get("code")
    if code is None:
        abort(500)
    api_tokens = discord_api.get_oauth_tokens(code)
    user_info = discord_api.get_user_info(api_tokens["access_token"])
    user = db.get_user_by_discord_id(int(user_info["id"]))
    if user is None:
        user = db.create_user(int(user_info["id"]), api_tokens["access_token"], api_tokens["refresh_token"])
    session["user_id"] = user.id
    session["user_discord_id"] = user.discord_id
    session["user_name"] = user_info['username']
    session["user_avatar"] = user_info['avatar']
    return redirect(url_for("mainpage"))
