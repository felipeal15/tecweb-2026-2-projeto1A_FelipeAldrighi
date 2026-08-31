from html import escape

from database import Database, Note
from utils import build_response, extract_params, load_template

db = Database('data/banco')

HTML_HEADER = 'Content-Type: text/html; charset=utf-8'
ERRO_CAMPOS_VAZIOS = 'Escreva um título e um conteúdo para salvar a anotação.'


# ---------------------------------------------------------------------------
# Views (uma por rota). Cada uma recebe a requisição e devolve bytes prontos.
# ---------------------------------------------------------------------------

def index(request):
    """GET  /  -> mural com todas as anotações.
       POST /  -> cria uma anotação nova."""
    if request.startswith('POST'):
        titulo, detalhes = _campos_do_formulario(request)

        if not titulo or not detalhes:
            return _pagina_inicial(ERRO_CAMPOS_VAZIOS, titulo, detalhes)

        db.add(Note(title=titulo, content=detalhes))
        return _redireciona('/')

    return _pagina_inicial()


def edit(request, note_id):
    """GET  /edit/<id>  -> formulário preenchido com a anotação.
       POST /edit/<id>  -> salva as alterações."""
    note = _busca_anotacao(note_id)
    if note is None:
        return not_found(request)

    if request.startswith('POST'):
        titulo, detalhes = _campos_do_formulario(request)

        if not titulo or not detalhes:
            return _pagina_edicao(note, ERRO_CAMPOS_VAZIOS, titulo, detalhes)

        note.title = titulo
        note.content = detalhes
        db.update(note)
        return _redireciona('/')

    return _pagina_edicao(note, '', note.title, note.content)


def delete(request, note_id):
    """GET  /delete/<id>  -> pede confirmação, mostrando a anotação.
       POST /delete/<id>  -> apaga de verdade (botão "Sim, apagar")."""
    note = _busca_anotacao(note_id)
    if note is None:
        return not_found(request)

    if request.startswith('POST'):
        db.delete(note.id)
        return _redireciona('/')

    corpo = load_template('confirm_delete.html').format(
        id=note.id,
        title=escape(note.title or ''),
        content=escape(note.content or ''),
    )
    return _pagina('Apagar anotação', corpo)


def favorite(request, note_id):
    """POST /favorite/<id> -> marca/desmarca a anotação como favorita."""
    note = _busca_anotacao(note_id)
    if note is None:
        return not_found(request)

    db.toggle_favorita(note.id)
    return _redireciona('/')


def not_found(request):
    """Qualquer rota desconhecida cai aqui."""
    return _pagina('Página não encontrada', load_template('404.html'),
                   code=404, reason='Not Found')


# ---------------------------------------------------------------------------
# Funções auxiliares: montam as páginas a partir dos templates
# ---------------------------------------------------------------------------

def _pagina(titulo, conteudo, code=200, reason='OK'):
    """Encaixa o conteúdo de uma página dentro do layout de base."""
    html = load_template('base.html').format(title=titulo, content=conteudo)
    return build_response(html, code=code, reason=reason, headers=HTML_HEADER)


def _pagina_inicial(erro='', titulo='', detalhes=''):
    corpo = load_template('index.html').format(
        erro=_mensagem_de_erro(erro),
        titulo=escape(titulo),
        detalhes=escape(detalhes),
        notes=_lista_de_anotacoes(),
    )
    return _pagina('Get-it', corpo)


def _pagina_edicao(note, erro='', titulo='', detalhes=''):
    corpo = load_template('edit.html').format(
        id=note.id,
        erro=_mensagem_de_erro(erro),
        titulo=escape(titulo or ''),
        detalhes=escape(detalhes or ''),
    )
    return _pagina('Editando anotação', corpo)


def _lista_de_anotacoes():
    notes = db.get_all()
    if not notes:
        return '        <p class="card-vazio">Nenhuma anotação ainda. Escreva a primeira!</p>'

    note_template = load_template('components/note.html')
    cards = [
        note_template.format(
            id=note.id,
            title=escape(note.title or ''),
            content=escape(note.content or ''),
            favorita='card-favorita' if note.favorita else '',
            favorita_icone='&#9733;' if note.favorita else '&#9734;',
            favorita_titulo='Desfavoritar' if note.favorita else 'Favoritar',
        )
        for note in notes
    ]
    return '\n'.join(cards)


def _mensagem_de_erro(erro):
    if not erro:
        return ''
    return f'        <p class="form-error">{escape(erro)}</p>'


def _campos_do_formulario(request):
    params = extract_params(request)
    return params.get('titulo', '').strip(), params.get('detalhes', '').strip()


def _busca_anotacao(note_id):
    """Converte o trecho da URL em id e devolve a anotação (ou None)."""
    try:
        return db.get(int(note_id))
    except (TypeError, ValueError):
        return None


def _redireciona(destino):
    return build_response(code=303, reason='See Other',
                          headers=f'Location: {destino}')
