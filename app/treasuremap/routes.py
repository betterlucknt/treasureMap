from flask import render_template, redirect, url_for, flash, request, jsonify
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user
from flask_babel import _
import sqlalchemy as sa
from app import db
from app.treasuremap import bp
from datetime import datetime, timedelta

COUNTDOWN_MINUTES = 50
COUNTDOWN_ADD = 10
COUNTDOWN_SUBSTRACT = 10
START_STEP = 5


scenes = {
    1: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Hola nens i nenes de la Terra, us contactem desde el món dels unicorns perquè necessitem la vostre ajuda!!
Un cièntific boig vol crear un raig per destruïr el Sol i per aconseguir-ho necessita el poder de les gemmes màgiques del nostre món. No sabem com ha aconseguit arribar al món Unicorn i nosaltres hem hagut d'amagar les gemmes a la Terra per tal de protegir-les. El científic boig es diu Doctor Xoriçó i ha espatllat el mecanisme que ens ha permés obrir el portal per enviar-vos les gemmes i ara no tenim prou màgia per venir-les a buscar. Hem pogut enviar 4 gemmes, la Gemma del Nord, la del Sud, la de l'Est i la de l'Oest, però sense elles no podem reparar el portal, només hem aconseguit enviar-vos un petit teletransportador que comunica la Terra amb el món dels Unicorns. Necessitem que vosaltres les trobeu i les poseu al teletransportador per tal que ens arribin i junts poguem vèncer el Dr. Xoriço. Compte!! ara no sabem on pare aquest Dr. torrat i podria estar aprop vostre també buscant les gemmes, de ben segur que haurà posat trampes per si algú més les està buscant. Nosaltres sabem a on són les 4 gemmes però per si el Dr. Xoriço està espiant no us podem dir a on s'amaguen, però si us hem deixat un mapa i pistes perquè les pogueu trobar totes. Seguiu el mapa i si us perdeu no dubteu a preguntar a través de l'ordinador, la nostre mascota Popunicorn us ajudarà sempre que pugui. Sempre que poguem ens comunicarem a través de l'ordinador de la Base Secreta on us trobeu ara, molta sort!''',
        "question": "", 
        "answer": "", 
    },
    2: {
        "image": "images/cute baby unicorn (1).jpeg",
        "text": '''''',
        'octocorn': '''Hi ha alguna "illa" en aquesta casa?''',
        'octocorn_image': "images/sticker_28.avif",
        "question": "", 
        "answer": "", 
    },
    3: {
        "image": "images/Designer (24).jpeg",
        "text": f'''''',
        'octocorn': '''Crec que "Cofre" i "Nuvols" estan a la sopa''',
        'octocorn_image': "images/sticker_2.avif",
        "question": "", 
        "answer": "", 
    },
    4: {
        "image": "images/Designer (26).jpeg",
        "text": f'''''',
        'octocorn': '''"Nuvols" és la última paraula de la frase''',
        'octocorn_image': "images/sticker_20.avif",
        "question": "", 
        "answer": "", 
    },
    5: {
        "image": "images/Dr_xorico1.jpeg",
        "text": f'''Heu estat contagiats per un virus i us queden {COUNTDOWN_MINUTES} min abans no faci efecte i us quedeu adormits per mesos. Ja ja ja, les gemes seran meves.''',
        "question": "", 
        "answer": "", 
    },
    6: {
        "image": "images/sticker_10.avif",
        "text": f'''Ostres no, el Dr. Xoriço ens ha enganyat, però no us preocupeu, els unicorns us prepararem l'antidot per parar el virus. 
        Vosaltres seguiu buscant les gemes que no queda gaire temps. Seguiu el Mapa! ''',
        "question": "", 
        "answer": "", 
    },
    7: {
        "image": "images/cute baby unicorn (3).jpeg",
        "text": "",
        'octocorn': '''Un dels Pokemons és Psyduck''',
        'octocorn_image': "images/sticker_21.avif",
        "question": "", 
        "answer": "", 
    },
    8: {
        "image": "images/Designer (13).jpeg",
        "text": "Oh no! el DR. Xoriço està començant a tapar el sol utilitzant energia que ha robat del nostre món, afanyeu-vos, necessitem les gemmes o aquest malvat es sortirà amb la seva. Sort que teniu les llanternes per poder veure a la foscor! Utilitzeu-les per seguir el mapa.",
        "audio": "audios/thunder.mp3",
        "question": "", 
        "answer": "", 
    },
    9: {
        "image": "images/Designer (27).jpeg",
        "text": "",
        'octocorn': '''Quan a l'estiu fa molta calor, els gelats els guardem al........''',
        'octocorn_image': "images/sticker_11.avif",
        "question": "", 
        "answer": "", 
    },
    10: {
        "image": "images/Designer (30).jpeg",
        "text": "Moltes gràcies, amb la gemma de l'Est tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant les altres gemmes. Molta sort!",
        "question": "", 
        "answer": "", 
    },
    11: {
        "image": "images/Designer (29).jpeg",
        "text": '''Com el nostre poder prové de la llum dels arcs de Sant Martí, haureu de recordar la seqüencia de llums en l'ordre correcte. Si ho aconseguiu obtindreu el codi.''',
        "question": "", 
        "answer": "", 
    },
    12: {
        "image": "images/Designer (12).jpeg",
        "text": '''Moltes gràcies, amb la gemma del Nord tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant les altres gemmes. Molta sort!''',
        "question": "", 
        "answer": "", 
    },
    13: {
        "image": "images/cute baby unicorn (2).jpeg",
        "text": '''''',
        'octocorn': '''Hi ha alguna X en aquesta casa?''',
        'octocorn_image': "images/sticker_10 (1).avif",
        "question": "", 
        "answer": "", 
    },
    14: {
        "image": "images/Designer (25).jpeg",
        "text": '''Moltes gràcies, amb la gemma de l'Oest tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant la última gemma. Molta sort!''',
        "question": "", 
        "answer": "", 
    },
    15: {
        "image": "images/Designer (28).jpeg",
        "text": '''El Dr. Xoriço va aconseguir estripar un troç del mapa, però no us preocupeu, amb tot el que heu aconseguit ja podeu trobar quin lloc indicava el mapa. No tardeu que encara heu de superar alguna prova per aconguir la Gemma del Sud!''',
        "question": "", 
        "answer": "", 
    },
    16: {
        "image": "images/cute baby unicorn (1).jpeg",
        "text": '''''',
        'octocorn': '''Quines peces encara no heu utilitzat?''',
        'octocorn_image': "images/sticker_5.avif",
        "question": "", 
        "answer": "", 
    },
    17: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Moltes gràcies, amb la gemma del Sud ja hem recuperat tot el nostre poder. Ara el DR. Xoriço ja no podrà apagar el sol ni fer més malícies. Ràpid, pugeu tots a l'habitació de l'Alexandra, allà trobareu unes piruletes màgiques amb l'antídot pel virus.''',
        "question": "", 
        "answer": "", 
    }
}

# Temps de la compta enrere en segons
starting_time = datetime.now()
stopped_time = datetime.now()
time_stopped = True
game_started = False
end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
current_step = 1
show_octocorn = 'none'
needs_redirect_admin = False
needs_redirect_user = False


@bp.route('/')
def treasuremap_home():
    return redirect(url_for('treasuremap.scene'))

@bp.route('/scene', methods=['GET', 'POST'])
def scene():
    global current_step
    global show_octocorn
    global time_stopped
    global game_started
    global end_time
    global needs_redirect_user
    needs_redirect_user = False
    if request.method == 'POST':
        answer = request.form.get('answer')
        if scenes[current_step]["answer"] == '' or answer.lower() == scenes[current_step]["answer"].lower():
            show_octocorn = False
            if(current_step < len(scenes)):
                current_step += 1
            if(current_step > START_STEP):
                
                end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
                time_stopped = False
                game_started = True
                    
            return redirect('/treasuremap/scene')
    return render_template('treasuremap/scene.html', scenes=scenes, current_step=current_step)

@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    global current_step
    global needs_redirect_admin
    needs_redirect_admin = False
    return render_template('treasuremap/admin.html', scenes=scenes, current_step=current_step)

@bp.route('/countdown')
def countdown():
    global end_time
    global stopped_time
    global time_stopped

    if(time_stopped):
        time_left = (end_time - stopped_time).total_seconds()
    else:
        time_left = (end_time - datetime.now()).total_seconds()
    
    if(time_left < 0):
        time_left = 0.0

    print(f'falten {time_left} segons')
    return str(f'{int(time_left/60):02}:{int(time_left - 60*int(time_left/60)):02}')

@bp.route('/restart')
def restart():
    global starting_time
    global end_time
    global current_step
    global show_octocorn
    global time_stopped
    global needs_redirect_admin
    global needs_redirect_user
    global game_started

    game_started = False
    needs_redirect_admin = True
    needs_redirect_user = True
    time_stopped = True
    current_step = 1
    starting_time = datetime.now()
    end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
    show_octocorn = False
    return (str(True))

@bp.route('/add_time')
def add_time():
    global end_time
    end_time = end_time + timedelta(minutes=COUNTDOWN_ADD)
    return str(True)

@bp.route('/add_time_5')
def add_time_5():
    global end_time
    end_time = end_time + timedelta(minutes=5)
    return str(True)

@bp.route('/add_time_1')
def add_time_1():
    global end_time
    end_time = end_time + timedelta(minutes=1)
    return str(True)

@bp.route('/stop_time')
def stop_time():
    global stopped_time
    global time_stopped

    time_stopped = True
    stopped_time = datetime.now()
    return str(True)

@bp.route('/resume_time')
def resume_time():
    global starting_time
    global end_time
    global time_stopped
    global stopped_time

    time_stopped = False
    time_diff = datetime.now() - stopped_time
    starting_time += time_diff
    end_time += time_diff
    return str(True)

@bp.route('/substract_time')
def substract_time():
    global end_time
    end_time = end_time - timedelta(minutes=COUNTDOWN_SUBSTRACT)
    return str(True)

@bp.route('/substract_time_5')
def substract_time_5():
    global end_time
    end_time = end_time - timedelta(minutes=5)
    return str(True)

@bp.route('/substract_time_1')
def substract_time_1():
    global end_time
    end_time = end_time - timedelta(minutes=1)
    return str(True)

@bp.route('/advance_scene')
def advance_scene():
    global current_step
    global show_octocorn
    global needs_redirect_admin
    global needs_redirect_user
    global game_started
    global time_stopped
    global end_time

    if current_step < len(scenes):
        show_octocorn = False
        current_step +=1
        needs_redirect_admin = True
        needs_redirect_user = True
        if(current_step == START_STEP):
            end_time = datetime.now() + timedelta(minutes=COUNTDOWN_MINUTES)
            time_stopped = False
            game_started = True

    return str(current_step)

@bp.route('/retrace_scene')
def retrace_scene():
    global current_step
    global show_octocorn
    global needs_redirect_admin
    global needs_redirect_user

    if current_step > 1:
        show_octocorn = False
        current_step -=1
        needs_redirect_admin = True
        needs_redirect_user = True
        
    return str(current_step)

@bp.route('/check_octocorn_status')
def check_octocorn_status():
    global show_octocorn
    return jsonify({'show_octocorn': show_octocorn})  

@bp.route('/show_octocorn_help')
def show_octocorn_help():
    global show_octocorn
    show_octocorn = True
    return str(show_octocorn)

@bp.route('/hide_octocorn_help')
def hide_octocorn_help():
    global show_octocorn
    show_octocorn = False
    return str(show_octocorn)

@bp.route('/needs_redirect')
def needs_redirect():
    global needs_redirect_admin
    global needs_redirect_user
    return jsonify({'needs_redirect_user': needs_redirect_user, 'needs_redirect_admin': needs_redirect_admin})  