from flask import render_template, redirect, url_for, flash, request, abort
from siteum import app, database, bcrypt
from siteum.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from siteum.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/sobre')
def sobre():
    caminho_do_arquivo = os.path.join(BASE_DIR, "texto2.md")
        
    if os.path.exists(caminho_do_arquivo):
        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_puro = arquivo.read()
        texto_convertido = markdown.markdown(conteudo_puro)
    else:
        texto_convertido = f"<p>Erro: O arquivo não foi encontrado em: {caminho_do_arquivo}</p>"
    
    return render_template('sobre.html', texto_doc=texto_convertido)

@app.route('/otrabalho')
def otrabalho():
    caminho_do_arquivo = os.path.join(BASE_DIR, "texto3.md")
        
    if os.path.exists(caminho_do_arquivo):
        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_puro = arquivo.read()
        texto_convertido = markdown.markdown(conteudo_puro)
    else:
        texto_convertido = f"<p>Erro: O arquivo não foi encontrado em: {caminho_do_arquivo}</p>"
    
    return render_template('otrabalho.html', texto_doc=texto_convertido)

@app.route('/quemsoueu')
def quemsoueu():
    caminho_do_arquivo = os.path.join(BASE_DIR, "texto4.md")
            
    if os.path.exists(caminho_do_arquivo):
        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_puro = arquivo.read()
        texto_convertido = markdown.markdown(conteudo_puro)
    else:
        texto_convertido = f"<p>Erro: O arquivo não foi encontrado em: {caminho_do_arquivo}</p>"
    
    return render_template('quemsoueu.html', texto_doc=texto_convertido)

@app.route('/apresentacao')
def apresentacao():
    caminho_do_arquivo = os.path.join(BASE_DIR, "texto1.md")
    
    # Verifica de forma simples se o arquivo existe (evita o try/except problemático)
    if os.path.exists(caminho_do_arquivo):
        with open(caminho_do_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo_puro = arquivo.read()
        texto_convertido = markdown.markdown(conteudo_puro)
    else:
        texto_convertido = f"<p>Erro: O arquivo não foi encontrado em: {caminho_do_arquivo}</p>"
 
    return render_template('apresentacao.html', texto_doc=texto_convertido)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if request.method == 'GET':

        email = request.args.get('email')

        if email:
            form_login.email.data = email

    foco_senha = request.args.get('foco_senha') == '1'

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(
            email=form_login.email.data
        ).first()

        if usuario and bcrypt.check_password_hash(
            usuario.senha,
            form_login.senha.data
        ):

            login_user(
                usuario,
                remember=form_login.lembrar_dados.data
            )

            flash(
                f'Login feito com sucesso no e-mail: {form_login.email.data}',
                'alert-success'
            )

            par_next = request.args.get('next')

            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))

        else:

            flash('Falha no Login', 'alert-danger')


    return render_template(
        'login.html',
        form_login=form_login,
        foco_senha=foco_senha
    )
    

@app.route('/pcriarconta', methods=['GET', 'POST'])
def criarconta():

    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:

        senha_cript = bcrypt.generate_password_hash(
            form_criarconta.senha.data
        ).decode("utf-8")

        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )

        database.session.add(usuario)
        database.session.commit()

        flash(
            f'Conta criada para o e-mail: {form_criarconta.email.data}',
            'alert-success'
        )

        return redirect(
            url_for(
                'login',
                email=form_criarconta.email.data,
                foco_senha=1
            )
        )

    return render_template(
        'pcriarconta.html',
        form_criarconta=form_criarconta
    )

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post enviado com Sucesso', 'alert-sucess')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)

    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

@app.route('/usuario/<int:usuario_id>/excluir', methods=['POST'])
@login_required
def excluir_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    try:
        Post.query.filter_by(id_usuario=usuario.id).delete()
        database.session.delete(usuario)
        database.session.commit()

        flash('Usuário excluído com sucesso!', 'alert-success')

    except Exception as erro:
        database.session.rollback()
        print(f'ERRO AO EXCLUIR USUÁRIO: {erro}')
        flash('Erro ao excluir usuário.', 'alert-danger')

    return redirect(url_for('usuarios'))

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
