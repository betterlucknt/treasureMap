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
START_STEP = 3

# TODO:
#        - Reordenar ajudes cornipulpo
#        - imatges adients
#        - Posar alguna gemma en la pagina
#        - Posar les gemmes que s-activin a mida que les aconsegueixen
#        - Posar opcio d'afegir o treure temps en la config de la prova
#        - Afegir proba buida quan no hagin de fer servir el ordi
#        - Add temps en step per mirar si poden demanar pista('popunicorn') o no
# Audios: octocorn->baby; drxorç->prot.Tone34.chitter77


scenes = {
    1: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Hola nens i nenes de la Terra, us contactem desde el món dels unicorns perquè necessitem la vostre ajuda!!
Un cièntific boig vol crear un raig per destruïr el Sol i per aconseguir-ho necessita el poder de les gemmes màgiques del nostre món. No sabem com ha aconseguit arribar al món Unicorn i nosaltres hem hagut d'amagar les gemmes a la Terra per tal de protegir-les. El científic boig es diu Doctor Xoriçó i ha espatllat el mecanisme que ens ha permés obrir el portal per enviar-vos les gemmes i ara no tenim prou màgia per venir-les a buscar. Hem pogut enviar 4 gemmes, la Gemma del Nord, la del Sud, la de l'Est i la de l'Oest, però sense elles no podem reparar el portal, només hem aconseguit enviar-vos un petit teletransportador que comunica la Terra amb el món dels Unicorns. Necessitem que vosaltres les trobeu i les poseu al teletransportador per tal que ens arribin i junts poguem vèncer el Dr. Xoriço. Compte!! ara no sabem on pare aquest Dr. torrat i podria estar aprop vostre també buscant les gemmes, de ben segur que haurà posat trampes per si algú més les està buscant. Nosaltres sabem a on són les 4 gemmes però per si el Dr. Xoriço està espiant no us podem dir a on s'amaguen, però si us hem deixat un mapa i pistes perquè les pogueu trobar totes. Seguiu el mapa i si us perdeu no dubteu a preguntar a través de l'ordinador, la nostre mascota Popunicorn us ajudarà sempre que pugui. Sempre que poguem ens comunicarem a través de l'ordinador de la Base Secreta on us trobeu ara, molta sort!''',
        'octocorn': '''Hi ha alguna "illa" en aquesta casa?''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    2: {
        "image": "images/Designer (27).webp",
        "text": f'''Dr. Xoriço: Heu estat contagiats per un virus i us queden {COUNTDOWN_MINUTES} min abans no faci efecte i us quedeu adormits per mesos. Ja ja ja, les gemes seran meves.''',
        'octocorn': '''"Nuvols" és la última paraula de la frase''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    2: {
        "image": "images/sticker_1.avif",
        "text": f'''Popunicorn: Ostres no, el Dr. Xoriço ens ha enganyat, però no us preocupeu, els unicorns us prepararem l'antidot per parar el virus. Vosaltres seguiu buscant les gemes que no queda gaire temps. Seguiu el Mapa! ''',
        'octocorn': '''"Nuvols" és la última paraula de la frase''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    3: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": "Oh no! el DR. Xoriço està començant a tapar el sol utilitzant energia que ha robat del nostre món, afanyeu-vos, necessitem les gemmes o aquest malvat es sortirà amb la seva.",
        'octocorn': '''Un dels Pokemons és Psyduck''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    4: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": "Moltes gràcies, amb la gemma de l'Est tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant les altres gemmes. Molta sort!",
        "question": "", 
        "answer": "", 
    },
    5: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Com el nostre poder prové de la llum dels arcs de Sant Martí, haureu de recordar la seqüencia de llums en l'ordre correcte. Si ho aconseguiu obtindreu el codi.''',
        "question": "", 
        "answer": "", 
    },
    6: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Moltes gràcies, amb la gemma del Nord tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant les altres gemmes. Molta sort!''',
        "question": "", 
        "answer": "", 
    },
    7: {
        "image": "images/cute_baby_unicorn.jpeg",
        "text": '''Moltes gràcies, amb la gemma de l'Oest tornem a tenir una mica de màgia per poder-vos ajudar. Amb això podem retressar una estona l'efecte del virus, ara teniu 10 min més per seguir buscant la última gemma. Molta sort!''',
        'octocorn': '''Hi ha alguna X en aquesta casa?''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    8: {
        "image": "images/sticker_1.avif",
        "text": '''El Dr. Xoriço va aconseguir estripar un troç del mapa, però no us preocupeu, amb tot el que heu aconseguit ja podeu trobar quin lloc indicava el mapa. No tardeu que encara heu de superar alguna prova per aconguir la Gemma del Sud!''',
        'octocorn': '''Quines peces encara no heu utilitzat?''',
        'octocorn_image': "images/sticker_1.avif",
        "question": "", 
        "answer": "", 
    },
    9: {
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
    global needs_redirect_user
    needs_redirect_user = False
    if request.method == 'POST':
        answer = request.form.get('answer')
        if scenes[current_step]["answer"] == '' or answer.lower() == scenes[current_step]["answer"].lower():
            show_octocorn = False
            if(current_step < len(scenes)):
                current_step += 1
            if(current_step > START_STEP):
                time_stopped = False
                game_started = True
                    
            return redirect('/treasuremap/scene')
    return render_template('treasuremap/scene.html', scene=scenes[current_step], current_step=current_step)

@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    global current_step
    global needs_redirect_admin
    needs_redirect_admin = False
    return render_template('treasuremap/admin.html', scene=scenes[current_step], current_step=current_step)

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

@bp.route('/advance_scene')
def advance_scene():
    global current_step
    global show_octocorn
    global needs_redirect_admin
    global needs_redirect_user
    global game_started
    global time_stopped

    if current_step < len(scenes):
        show_octocorn = False
        current_step +=1
        needs_redirect_admin = True
        needs_redirect_user = True
        if(current_step > START_STEP):
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