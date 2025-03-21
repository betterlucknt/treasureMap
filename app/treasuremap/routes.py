from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.treasuremap import bp

scenes = {
    1: {
        "image": "scene1.jpg",
        "text": "Benvingut a la primera escena!",
        "font_size": "20px",
        "font_family": "Arial",
        "groups": [
            {"question": "Quina és la capital de França?", "answer": "París", "next_scene": 2}
        ]
    },
    2: {
        "image": "scene2.jpg",
        "text": "Has arribat a la segona escena!",
        "font_size": "20px",
        "font_family": "Arial",
        "groups": [
            {"question": "Quin és el riu més llarg del món?", "answer": "Amazones", "next_scene": 3}
        ]
    }
}

# Temps de la compta enrere en segons
countdown_time = 600  # 10 minuts


@bp.route('/')
def treasuremap_home():
    return redirect(url_for('scene', scene_id=1))

@bp.route('/scene/<int:scene_id>', methods=['GET', 'POST'])
def scene(scene_id):
    global countdown_time
    if request.method == 'POST':
        answer = request.form.get('answer')
        for group in scenes[scene_id]["groups"]:
            if answer.lower() == group["answer"].lower():
                return redirect(url_for('scene', scene_id=group["next_scene"]))
    print(scenes[scene_id])
    return render_template('treasuremap/scene.html', scene=scenes[scene_id], countdown_time=countdown_time)

@bp.route('/countdown')
def countdown():
    global countdown_time
    countdown_time -= 1
    print(countdown)
    return str(countdown_time)