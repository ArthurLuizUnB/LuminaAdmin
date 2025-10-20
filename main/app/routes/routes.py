from flask import Blueprint, render_template, request, redirect, url_for, flash

routes = Blueprint('routes', __name__)

# Rota principal para o Painel Administrativo do Lumina Admin (URL raiz)
@routes.route('/', methods=['GET', 'POST'])
def admin_panel():
    # SIMULAÇÃO DE DADOS DE ARTIGOS (MOCKUP: RF-006.1 e RF-006.2)
    # Estes dados simulam o conteúdo que viria do banco de dados (ID, título, fonte e link)
    artigos_mock = [
        {
            "id": "1",
            "titulo": "Por que especialistas dizem que inteligência artificial pode levar à extinção da humanidade",
            "fonte": "BBC News Brasil",
            "link": "https://www.bbc.com/portuguese/articles/c51q3jvlyj8o"
        },
        {
            "id": "2",
            "titulo": "Tribunal dos EUA proíbe NSO Group de instalar software espião no WhatsApp",
            "fonte": "Folha de S.Paulo",
            "link": "https://www1.folha.uol.com.br/tec/2025/10/tribunal-dos-eua-proibe-nso-group-de-instalar-software-espiao-no-whatsapp.shtml"
        },
        {
            "id": "3",
            "titulo": "Cessar-fogo entre Israel e Hamas é vitória para o povo palestino, porém “relativa e triste”, avalia docente da Unesp",
            "fonte": "Jornal da Unesp",
            "link": "https://jornal.unesp.br/2025/10/14/cessar-fogo-entre-israel-e-hamas-e-vitoria-para-o-povo-palestino-porem-relativa-e-triste-avalia-docente-da-unesp/"
        },
    ]

    # Nome do usuário mock, injetado no template para simular o estado "logado como admin"
    usuario_nome = "Administrador Lumina"
    
    # RF-006.3: Lógica para Adicionar Novo Artigo (Esqueleto POST)
    if request.method == 'POST':
        if 'link_artigo' in request.form:
            # Lógica temporária para simular a adição do link ao BD
            link_novo_artigo = request.form['link_artigo']
            
            # RF-006.4: Confirmação Visual usando Flask flash
            flash(f'Artigo (Link: {link_novo_artigo}) adicionado com sucesso!', 'success')
            return redirect(url_for('routes.admin_panel'))
    
    # RF-006.6: Lógica do Campo de Busca/Filtro (GET)
    search_query = request.args.get('search', '').lower()
    if search_query:
        # Filtra os artigos que contêm o termo de busca no título ou fonte
        artigos_filtrados = [
            a for a in artigos_mock 
            if search_query in a['titulo'].lower() or search_query in a['fonte'].lower()
        ]
    else:
        artigos_filtrados = artigos_mock

    # Renderiza o template principal do Lumina Admin
    return render_template("lumina_admin.html", artigos=artigos_filtrados, usuario_nome=usuario_nome)

# RF-006.5: Rota para Remover Artigo (Esqueleto)
@routes.route('/remover/<artigo_id>')
def remover_artigo(artigo_id):
    # Lógica temporária para simular a remoção do artigo
    flash(f'Artigo com ID "{artigo_id}" removido com sucesso!', 'success')
    return redirect(url_for('routes.admin_panel'))