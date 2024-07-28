from os import getenv

from flask import request, render_template, session, redirect, url_for, abort, jsonify

from src.webapp import db, discord_api


def mainpage():
    return render_template("index.j2")


def gallery():
    user = db.get_user_by_id(session['user_id'])
    user_servers = discord_api.get_user_guilds(user.access_token)
    servers_with_pics: list[dict] = []
    for server in user_servers:
        server_in_db = db.get_server_by_discord_id(server["id"])
        if server_in_db is None:
            continue
        channels = db.get_channels_in_server(server_in_db.id)
        enabled_channels = [channel for channel in channels if channel.enabled]
        if not enabled_channels:
            continue
        channels_json = [
            {
                "id": channel.id,
                "name": discord_api.get_channel_info(channel.discord_id)["name"],
            } for channel in enabled_channels
        ]
        servers_with_pics.append({
            "id": server_in_db.id,
            "discord_id": server_in_db.discord_id,
            "name": server["name"],
            "icon": server["icon"],
            "channels": channels_json
        })

    return render_template("gallery.j2", guilds=servers_with_pics)


def server_channels():
    server_id = request.args.get("server_id")
    server = db.get_server_by_discord_id(server_id)
    channels = db.get_channels_in_server(server.id)
    channels_json = []
    for channel in channels:
        channel_info = discord_api.get_channel_info(channel.discord_id)
        channels_json.append({
            "id": channel.id,
            "enabled": channel.enabled,
            "name": channel_info["name"],
        })
    return jsonify(channels_json)


def update_channel():
    data = request.get_json()
    channel = db.get_channel_by_id(data["id"])
    db.update_channel(data["id"], discord_id=channel.discord_id, enabled=data["new_state"], server_id=channel.server_id)
    return ""


@login_required
def management():
    user = db.get_user_by_id(session['user_id'])
    user_guilds = discord_api.get_user_guilds(user.access_token)
    user_managed_guilds = [guild for guild in user_guilds if int(guild["permissions"]) & 32]
    print(user_managed_guilds)
    user_installed_guilds = []
    user_installable_guilds = []
    for guild in user_managed_guilds:
        guild_in_db = db.get_server_by_discord_id(guild["id"])
        if guild_in_db is None:
            user_installable_guilds.append(guild)
        else:
            user_installed_guilds.append(guild)
    return render_template("management.j2", installable_guilds=user_installable_guilds,
                           installed_guilds=user_installed_guilds)


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


def install_redirect():
    return redirect(f"https://discord.com/oauth2/authorize?client_id={getenv("CLIENT_ID")}")
