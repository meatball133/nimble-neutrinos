from flask import request, render_template


def mainpage():
    return render_template("index.j2")


def gallery():
    return render_template("gallery.j2")


def management():
    return render_template("management.j2")