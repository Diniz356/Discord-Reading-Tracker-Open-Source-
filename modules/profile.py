import sqlite3
""" Funções de gereciamento de perfil e buscas de dados da tabela perfil em SQL"""


def save_bg(id,link):
    """     salva o url da imagem do comando estante

    :param id: id de identificação do usuário
    :param link: url da imagem de plano de fundo da estante
    :return: return para o arquivo principal
    """

    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = "SELECT background FROM perfil WHERE user_id = ?"
    cursor.execute(buscar,(id,))
    if cursor.fetchone() is None:
        inserir = "INSERT INTO perfil (background,user_id) VALUES (?,?)"
        cursor.execute(inserir, (link, id))
        db.commit()
        db.close()
        return
    else:
        mudar = "UPDATE perfil SET background = ? WHERE user_id = ?"
        cursor.execute(mudar,(link,id))
        db.commit()
        db.close()
        return

def save_pf(id,link):
    """     salva o url da imagem do fundo do comando perfil

        :param id: id de identificação do usuário
        :param link: url da imagem de plano de fundo da estante
        :return: return para o arquivo principal
        """

    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = "SELECT banner FROM perfil WHERE user_id = ?"
    cursor.execute(buscar,(id,))
    if cursor.fetchone() is None:
        inserir = "INSERT INTO perfil (user_id,banner) VALUES (?,?)"
        cursor.execute(inserir,(id,link))
        db.commit()
        return
    else:
        atualizar = "UPDATE perfil SET banner = ? WHERE user_id = ?"
        cursor.execute(atualizar,(link,id))
        db.commit()
        return

def user_bg(id):
    """     função de busca de imagem de fundo do comando estante

    :image_est var: recebe o url da imagem do fundo da estante
    :return: retorna o url da imagem para embed
    """
    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = "SELECT background FROM perfil WHERE user_id = ?"
    cursor.execute(buscar,(id,))
    image_est = cursor.fetchone()
    db.commit()
    if image_est is None:
        return "https://img.freepik.com/vetores-premium/faixas-diagonais-de-fundo-listrado-preto_322958-2715.jpg?semt=ais_hybrid&w=740&q=80"
    else:
        return image_est[0]

def user_pf(id):
    """     função de busca de imagem de fundo do comando perfil

    :image_pf var: recebe o url da imagem de fundo de perfil
    :return: retorna o url da imagem de fundo do perfil
    """

    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = "SELECT banner FROM perfil WHERE user_id = ?"
    cursor.execute(buscar,(id,))
    image_pf = cursor.fetchone()
    db.commit()
    if image_pf is None:
        return "https://img.freepik.com/vetores-premium/faixas-diagonais-de-fundo-listrado-preto_322958-2715.jpg?semt=ais_hybrid&w=740&q=80"
    else:
        return image_pf[0]