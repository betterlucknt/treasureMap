from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.treasuremap import bp
from datetime import datetime, timedelta

COUNTDOWN_MINUTES = 600
COUNTDOWN_ADD = 60
COUNTDOWN_SUBSTRACT = 60

# TODO:
#        - Add admin page
#        - Add all steps
#        - Add control extra time given or taken
#        - Add temps en step per mirar si poden demanar pista('popunicorn') o no


scenes = {
    1: {
        "image": "scene1.jpg",
        "text": '''Dr. Xoriço: Heu estat contagiats per un virus i us queden x min abans no faci efecte i us quedeu adormits per mesos. Ja ja ja, les gemes seran meves''',
        'Popunicorn': '''Ostres no, el Dr. Xoriço ens ha enganyat, però no us preocupeu, els unicorns us prepararem l'antidot per parar el virus. Vosaltres seguiu buscant les gemes que no queda gaire temps. Seguieu el Mapa!''',
        "font_size": "20px",
        "font_family": "Arial",
        "groups": [
            {"question": "La ____ del _____ està al ___ ___________ de Núvols", "answer": "La Clau del Cofre està al Pot Transparent de Núvols", "next_scene": 2}
        ]
    },
    2: {
        "image": "scene2.jpg",
        "text": "So de trons, el DR. Xoriço està començant a tapar el sol, a partir d'ara s'apaguen les llums i han d'utilitzar les llanternes",
        "font_size": "20px",
        "font_family": "Arial",
        "groups": [
            {"question": "So de trons", "answer": "Amazones", "next_scene": 3}
        ]
    },
    3: {
        "image": "scene2.jpg",
        "text": "So de trons, el DR. Xoriço està començant a tapar el sol, a partir d'ara s'apaguen les llums i han d'utilitzar les llanternes",
        "font_size": "20px",
        "font_family": "Arial",
        "groups": [
            {"question": "Unicorns: Moltes gràcies, amb aquesta gemma tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant les altres gemes. Molta sort!", "answer": "Amazones", "next_scene": 3}
        ]
    }
}

# Temps de la compta enrere en segons
starting_time = datetime.now()
end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
time_left = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
current_step = 1


@bp.route('/')
def treasuremap_home():
    return redirect(url_for('scene'))

@bp.route('/scene', methods=['GET', 'POST'])
def scene():
    global time_left
    global current_step
    if request.method == 'POST':
        answer = request.form.get('answer')
        for group in scenes[current_step]["groups"]:
            if answer.lower() == group["answer"].lower():
                return redirect(url_for('scene', scene_id=group["next_scene"]))
    print(scenes[current_step])
    return render_template('treasuremap/scene.html', scene=scenes[current_step], countdown_time=time_left)

@bp.route('/admin', methods=['GET', 'POST'])
def scene():
    return render_template('treasuremap/admin.html', countdown_time=time_left)

@bp.route('/countdown')
def countdown():
    global end_time
    global time_left
    time_left = (end_time - datetime.now()).total_seconds()/60

    print(f'falten {time_left} minuts')
    return str(time_left)

@bp.route('/start')
def start():
    global starting_time
    global end_time
    global time_left
    global current_step
    current_step = 1
    starting_time = datetime.now()
    end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
    time_left = COUNTDOWN_MINUTES
    return (True)