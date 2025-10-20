# main/app/routes/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
import json
import os
import uuid
from datetime import datetime

routes = Blueprint('routes', __name__)

# --- UTILITY: SIMULAÇÃO DO BANCO DE DADOS (DB_FILE) ---
# Define o caminho do arquivo db.json (o caminho real depende da sua estrutura)
# Vamos usar um caminho simplificado, assumindo que db.json está na raiz do projeto.
# Se estivesse no mesmo diretório do routes.py, seria assim:
# DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/db.json')
# Para simplificar neste ambiente, assumimos a localização conhecida:
DB_FILE = 'arthurluizunb/luminaadmin/LuminaAdmin-68aaf5020725026ea96b5ad004ef17737ea318b9/main/data/db.json'


def load_data():
    """Carrega os dados do db.json. Se o arquivo estiver vazio, inicializa a estrutura."""
    try:
        with open(DB_FILE, 'r') as f:
            data = json.load(f)
            # Garante que a chave 'artigos' exista, mesmo que o arquivo db.json original seja {}
            if 'artigos' not in data:
                data['artigos'] = []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Inicializa com a estrutura básica e os mocks
        return {
            "artigos": [
                {
                    "id": str(uuid.uuid4()),
                    "titulo": "Inteligência Artificial: O Novo Horizonte do Mercado de Trabalho",
                    "fonte": "Jornal de Tecnologia",
                    "link": "https://www.jornaltech.com/artigo1"
                },
                {
                    "id": str(uuid.uuid4()),
                    "titulo": "O Futuro da Computação em Nuvem e a Segurança de Dados Pessoais",
                    "fonte": "Site de Inovação",
                    "link": "https://www.inovacao.com/artigo2"
                },
                {
                    "id": str(uuid.uuid4()),
                    "titulo": "Análise do Setor de Data Science na América Latina",
                    "fonte": "Revista Científica",
                    "link": "https://www.revistacientifica.com/artigo3"
                },
            ]
        }


def save_data(data):
    """Salva os dados de volta no db.json com formatação bonita (indent=4)."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# --- ROTAS PRINCIPAIS ---

@routes.route('/', methods=['GET', 'POST'])
def admin_panel():
    # Carrega os dados persistidos (ou mock inicializados)
    data = load_data()
    artigos = data.get('artigos', [])
    usuario_nome = "Administrador Lumina" # Mock do nome do usuário

    # RF-006.3: Lógica para Adicionar Novo Artigo (Esqueleto POST)
    if request.method == 'POST':
        if 'link_artigo' in request.form:
            link_novo_artigo = request.form['link_artigo']
            
            # TODO: Aqui seria a lógica para extrair o título e fonte do link real.
            # Por enquanto, usamos dados mock e um ID UUID
            novo_artigo = {
                "id": str(uuid.uuid4()),
                "titulo": f"Novo Artigo (URL: {link_novo_artigo[:30]}...)",
                "fonte": "Fonte Não Especificada",
                "link": link_novo_artigo
            }
            
            artigos.append(novo_artigo)
            save_data(data) # Persiste o novo artigo
            
            # RF-006.4: Confirmação Visual
            flash(f'Artigo (Link: {link_novo_artigo}) adicionado com sucesso!', 'success')
            return redirect(url_for('routes.admin_panel'))
    
    # RF-006.6: Lógica do Campo de Busca/Filtro (GET)
    search_query = request.args.get('search', '').lower()
    if search_query:
        artigos_filtrados = [
            a for a in artigos 
            if search_query in a['titulo'].lower() or search_query in a['fonte'].lower()
        ]
    else:
        artigos_filtrados = artigos

    # Renderiza o template principal
    return render_template("lumina_admin.html", artigos=artigos_filtrados, usuario_nome=usuario_nome)

# RF-006.5: Rota para Remover Artigo (Esqueleto)
@routes.route('/remover/<artigo_id>')
def remover_artigo(artigo_id):
    data = load_data()
    artigos = data.get('artigos', [])
    
    # Encontra e remove o artigo pelo ID
    artigo_removido = next((a for a in artigos if a["id"] == artigo_id), None)
    
    if artigo_removido:
        data['artigos'] = [a for a in artigos if a["id"] != artigo_id]
        save_data(data) # Persiste a remoção
        flash(f'Artigo "{artigo_removido["titulo"]}" removido com sucesso!', 'success')
    else:
        flash(f'Artigo com ID "{artigo_id}" não encontrado.', 'error')
        
    return redirect(url_for('routes.admin_panel'))