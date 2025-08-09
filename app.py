from flask import Flask, render_template, request, redirect, url_for, session
import json
from datetime import datetime
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # troque por uma chave segura em produção

DB_PATH = 'database.json'

ASKMUSIC = ["La musica ha suscitato qualche emozione in te?", "Ti è piaciuta la voce del cantante o della cantante?", "Ascolteresti di nuovo questa canzone?", "Il testo trasmette un messaggio rilevante o interessante?", "La produzione musicale ti è sembrata ben fatta?", "Consiglieresti questa canzone a qualcuno?", "Il ritornello ti è rimasto in testa?", "La canzone ti ha ricordato qualche momento della tua vita?", "Lo stile della canzone corrisponde ai tuoi gusti personali?", "L’artista sembra avere un’identità propria?", "Hai percepito autenticità nell’interpretazione?", "La canzone è diversa da ciò che ascolti di solito?", "Il ritmo ti ha fatto venire voglia di ballare o muoverti?", "La canzone ha il potenziale per diventare un successo?", "La copertina o l’immagine dell’artista ha attirato positivamente la tua attenzione?", "Il testo è facile da capire e seguire?", "Ascolteresti questa canzone in diversi momenti della giornata?", "La canzone ti ha lasciato la voglia di conoscere meglio l’artista?", "La canzone trasmette qualche sentimento vero?", "La melodia è piacevole all’orecchio?", "C’è qualche parte della canzone che ti ha colpito particolarmente?", "Il videoclip (se presente) migliora l’esperienza?", "Credi che l’artista sia coerente con le sue altre canzoni?", "La canzone è originale rispetto ad altre dello stesso genere?", "Il ritmo o l’arrangiamento musicale ha attirato la tua attenzione in modo positivo?", "Ti immagini di aggiungere questa canzone a una delle tue playlist?", "Credi che l’artista abbia talento?", "La canzone ti ha sorpreso in qualche modo?", "Credi che l’artista abbia futuro nell’industria?", "Consiglieresti questa canzone o artista a qualcuno con gusti musicali diversi dai tuoi?"]
# ASKMUSIC = ["¿La música despertó alguna emoción en usted?", "¿Le agradó la voz del cantante o la cantante?", "¿Escucharía esta canción nuevamente?", "¿La letra transmite algún mensaje relevante o interesante?", "¿La producción musical le pareció bien hecha?", "¿Recomendaría esta canción a alguien?", "¿El estribillo se le quedó en la cabeza?", "¿La canción le recordó a algún momento de su vida?", "¿El estilo de la canción coincide con sus gustos personales?", "¿El artista parece tener una identidad propia?", "¿Sintió autenticidad en la interpretación?", "¿La canción es diferente a lo que suele escuchar?", "¿El ritmo le dio ganas de bailar o moverse?", "¿La canción tiene potencial para convertirse en un éxito?", "¿La portada o imagen del artista llamó positivamente su atención?", "¿La letra es fácil de entender y seguir?", "¿Escucharía esta canción en distintos momentos del día?", "¿La canción le dejó con ganas de conocer más del artista?", "¿La canción transmite algún sentimiento verdadero?", "¿La melodía es agradable al oído?", "¿Alguna parte de la canción le marcó especialmente?", "¿El videoclip (si lo hay) mejora la experiencia?", "¿Cree que el artista es consistente con otras canciones suyas?", "¿La canción es original en comparación con otras del mismo género?", "¿El ritmo o instrumental llamó su atención de forma positiva?", "¿Se imagina agregando esta canción a alguna de sus listas de reproducción?", "¿Cree que el artista tiene talento?", "¿La canción le sorprendió de alguna manera?", "¿Cree que el artista tiene futuro en la industria?", "¿Recomendaría esta canción o artista a alguien con gustos musicales diferentes a los suyos?"]
# ASKMUSIC = ["A música despertou alguma emoção em você?", "A voz do cantor/cantora te agradou?", "Você escutaria essa música de novo?", "A letra tem alguma mensagem relevante ou interessante?", "A produção musical pareceu bem feita?", "Você indicaria essa música para alguém?", "O refrão ficou na sua cabeça?", "A música te lembrou de algum momento da sua vida?", "O estilo da música combina com seu gosto pessoal?", "O artista parece ter identidade própria?", "Você sentiu autenticidade na performance?", "A música é diferente do que você costuma ouvir?", "O ritmo te fez querer dançar ou se mexer?", "A música tem potencial para se tornar um hit?", "A capa ou imagem do artista te chamou atenção positivamente?", "A letra é fácil de entender e acompanhar?", "Você escutaria essa música em diferentes momentos do dia?", "A música te deixou com vontade de conhecer mais do artista?", "A música passa algum sentimento verdadeiro?", "A melodia é agradável aos ouvidos?", "A música tem alguma parte que te marcou especialmente?", "O clipe (se houver) contribui positivamente para a experiência?", "Você acha que o artista é consistente com outras músicas dele(a)?", "A música é original em comparação com outras do mesmo gênero?", "A batida ou instrumental chamou sua atenção de forma positiva?", "Você se vê colocando essa música em uma playlist sua?", "Você acha que o artista tem talento?", "A música te surpreendeu de alguma forma?", "Você acha que o artista tem futuro na indústria?", "Você recomendaria essa música/artista para alguém com gosto musical diferente do seu?"]
# ASKMUSIC = ["Cette chanson a-t-elle réveillé une émotion chez toi ?", "As-tu aimé la voix du chanteur ou de la chanteuse ?", "Est-ce que tu écouterais cette chanson à nouveau ?", "Les paroles ont-elles un message intéressant ou important ?", "La production musicale te semble-t-elle bien faite ?", "Tu recommanderais cette chanson à quelqu’un ?", "Le refrain t’est-il resté dans la tête ?", "Cette chanson t’a-t-elle rappelé un moment de ta vie ?", "Le style musical correspond-il à tes goûts personnels ?", "L’artiste te semble-t-il avoir une identité propre ?", "As-tu ressenti de l’authenticité dans la performance ?", "Cette chanson est-elle différente de ce que tu écoutes d’habitude ?", "Le rythme t’a-t-il donné envie de danser ou bouger ?", "Tu penses que cette chanson peut devenir un hit ?", "La pochette ou l’image de l’artiste t’a-t-elle attiré positivement ?", "Les paroles sont-elles faciles à comprendre et à suivre ?", "Tu écouterais cette chanson à différents moments de la journée ?", "Cette chanson t’a-t-elle donné envie d’en découvrir plus sur l’artiste ?", "La chanson transmet-elle une émotion vraie ?", "La mélodie est-elle agréable à écouter ?", "Y a-t-il un passage de la chanson qui t’a marqué ?", "Le clip (s’il existe) améliore-t-il l’expérience ?", "Tu trouves que l’artiste est cohérent avec ses autres chansons ?", "Cette chanson est-elle originale par rapport à d’autres du même genre ?", "La rythmique ou l’instrumental t’a-t-elle marqué positivement ?", "Tu te vois ajouter cette chanson à l’une de tes playlists ?", "Tu trouves que l’artiste a du talent ?", "La chanson t’a-t-elle surpris(e) d’une certaine manière ?", "Tu penses que l’artiste a un avenir dans l’industrie musicale ?", "Tu recommanderais cette chanson/artiste à quelqu’un avec des goûts différents des tiens ?"]
IMGSRANDOM = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

def resetar_se_novo_dia(user):
    hoje = datetime.now().date().isoformat()
    if user.get('last_evaluation_date') != hoje:
        user['evaluations_today'] = 0
        user['earned_today'] = 0.0
        user['last_evaluation_date'] = hoje

# Função para carregar o banco de dados
def load_db():
    if not os.path.exists(DB_PATH):
        return {"users": {}}
    with open(DB_PATH, 'r') as file:
        return json.load(file)

# Função para salvar no banco de dados
def save_db(data):
    with open(DB_PATH, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db = load_db()
        user = db['users'].get(username)

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Nome utente o password non validi.")

    return render_template('login.html')

# Rota de cadastro
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if password != confirm_password:
        return render_template('login.html', error="Le password non coincidono.")

    db = load_db()

    if username in db['users']:
        return render_template('login.html', error="Il nome utente esiste già.")

    db['users'][username] = {
        "password": password,
        "paypal": "",
        "balance": 180.0,
        "withdrawn": 0.0,
        "created_at": datetime.now().isoformat(),
        "last_withdraw_date": None,
        "evaluations_today": 0
    }

    save_db(db)
    session['username'] = username
    return render_template('login.html', success="Nome utente creato con successo.")

# Rota do dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = load_db()
    username = session['username']
    user = db['users'].get(username)

    if not user:
        session.pop('username', None)
        return redirect(url_for('login'))


    # Verifica se já é outro dia e zera a contagem
    today = datetime.now().date().isoformat()
    if user.get("last_evaluation_date") != today:
        user["evaluations_today"] = 0
        user["earned_today"] = 0.0
        user["last_evaluation_date"] = today
        save_db(db)

    return render_template('dashboard.html', user=user, username=username)

@app.route('/rating')
def rating():
    if 'username' not in session:
        return redirect(url_for('login'))

    db = load_db()
    username = session['username']
    user = db['users'][username]

    # Resetar contadores se for novo dia
    resetar_se_novo_dia(user)

    # Verificação de limite
    if user['evaluations_today'] >= 16 or user['earned_today'] >= 120.0:
        save_db(db)  # salvar reset, se tiver sido feito
        return redirect(url_for('dashboard'))

    save_db(db)  # mesmo que não redirecione, salvar possíveis resets

    # Calcula avaliações restantes
    avaliacoes_restantes = 16 - user['evaluations_today']

    # Sorteia X perguntas e imagens aleatórias baseadas na quantidade faltante
    perguntas = random.sample(ASKMUSIC, avaliacoes_restantes)
    images = random.sample(IMGSRANDOM, avaliacoes_restantes)

    return render_template('rating.html', user=user, perguntas=perguntas, images=images, avaliacoes_restantes=avaliacoes_restantes)

from flask import jsonify

@app.route('/salvar-avaliacoes', methods=['POST'])
def salvar_avaliacoes():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        db = load_db()
        username = session['username']
        user = db['users'][username]

        today = datetime.now().date().isoformat()

        # Resetar contadores se for novo dia
        resetar_se_novo_dia(user)

        # Verificar se já atingiu o limite
        if user['evaluations_today'] >= 16 or user['earned_today'] >= 120.0:
            return jsonify(success=False, error="Limite giornaliero raggiunto.")

        # Atualiza os dados do usuário
        user['evaluations_today'] += 1
        user['earned_today'] += 7.5
        user['balance'] += 7.5
        user['last_evaluation_date'] = today

        save_db(db)
        return jsonify(success=True)
    
    except Exception as e:
        return jsonify(success=False, error=str(e))



# Rota de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Execução local
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
