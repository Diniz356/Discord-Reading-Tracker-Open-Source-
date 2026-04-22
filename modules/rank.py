import sqlite3

def xp_up(id,pglidas):
    novo_xp = pglidas * 10
    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = "SELECT totalxp FROM niveis WHERE user_id = ?"
    cursor.execute(buscar,(id,))
    if cursor.fetchone() is None:
        inserir = "INSERT INTO niveis (user_id,totalxp) VALUES (?,?)"
        cursor.execute(inserir,(id,novo_xp))
        db.commit()
    else:
        atualizar = "UPDATE niveis SET totalxp = totalxp + ? WHERE user_id = ?"
        cursor.execute(atualizar,(novo_xp,id))
        db.commit()
    db.close()
    return

def rankup(id):
    db = sqlite3.connect("Biblioteca.db")
    cursor = db.cursor()
    buscar = 'SELECT totalxp, nivel FROM niveis WHERE user_id = ?'
    cursor.execute(buscar,(id,))
    resultado = cursor.fetchone()
    if resultado and resultado[0] >= 1000:
        totalxp, nivel_atual = resultado
        niveis_ganhos = totalxp // 1000
        xp_restante = totalxp % 1000
        cursor.execute('UPDATE niveis SET totalxp = ?, nivel = nivel + ? WHERE user_id = ? ',(xp_restante,niveis_ganhos,id))
        db.commit()
        db.close()
        return True
    db.commit()
    db.close()
    return False

def user_rank(id):
    db = sqlite3.connect("Biblioteca.db")
    buscar = 'SELECT nivel FROM niveis WHERE user_id = ?'
    cursor = db.cursor()
    cursor.execute(buscar,(id,))
    rank = cursor.fetchone()
    db.close()
    return rank

def user_xp(id):
    db = sqlite3.connect("Biblioteca.db")
    buscar = 'SELECT totalxp FROM niveis WHERE user_id = ?'
    cursor = db.cursor()
    cursor.execute(buscar,(id,))
    xp = cursor.fetchone()
    db.close()
    return xp
