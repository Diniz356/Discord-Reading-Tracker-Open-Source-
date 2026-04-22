import discord
from discord.ext import commands
import sqlite3
from modules import profile
from modules import rank

intents = discord.Intents.all()
bot = commands.Bot(".",intents=intents)

@bot.event
async def on_ready():
    print("\033[01;32mBOT INICIALIZADO COM SUCESSO!\033[0m")
intents.message_content = True

db = sqlite3.connect('biblioteca.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        user_id INTEGER,
        titulo TEXT,
        paginas_totais INTEGER DEFAULT 0,
        paginas_lidas INTEGER DEFAULT 0
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS niveis (
        user_id INTEGER,
        totalxp INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS perfil (
        user_id INTEGER,
        banner TEXT,
        background TEXT
    )
''')
db.commit()

@bot.command()
async def registrar_livro(ctx,paginas_totais:int, *,titulo:str):
    user_id = ctx.author.id
    inserir = "INSERT INTO LIVROS (titulo,paginas_totais,user_id) VALUES (?,?,?)"
    cursor.execute(inserir, (titulo.lower().strip(),paginas_totais,user_id))
    db.commit()
    await ctx.send(f"✅ **O livro {titulo} foi inserido na sua biblioteca!**")

@bot.command()
async def apagar_livro(ctx, *,titulo:str):
    user_id = ctx.author.id
    cursor.execute("SELECT titulo FROM livros WHERE user_id = ? ",(user_id,))
    listalivro = cursor.fetchall()
    livros = []
    for c in range(len(listalivro)):
        livros.extend(listalivro[c])
    if titulo.lower() in livros:
        apagar = "DELETE FROM livros WHERE user_id = ? AND titulo = ?"
        cursor.execute(apagar,(user_id,titulo.strip().lower()))
        db.commit()
        await ctx.send(f"✅ **O livro {titulo.title()} foi apagado da sua biblioteca!**")
    else:
        await ctx.send(f"❓ **O livro {titulo} não pertence a sua biblioteca!**")

@bot.command()
async def ler(ctx,lido: int, *,titulo: str):
    user_id = ctx.author.id
    titulo_norm = titulo.lower().strip()
    buscar = "SELECT titulo FROM livros WHERE user_id = ?"
    cursor.execute(buscar,(user_id,))
    resultado_livros = cursor.fetchall()
    livros = []
    for c in resultado_livros:
        livros.extend(c)

    if titulo_norm in livros:
        buscatotal = "SELECT paginas_totais FROM livros WHERE user_id = ? AND titulo = ?"
        cursor.execute(buscatotal, (user_id, titulo_norm))
        resultado_total = cursor.fetchone()
        buscalido = "SELECT paginas_lidas FROM livros WHERE user_id = ? AND titulo = ?"
        cursor.execute(buscalido, (user_id, titulo_norm))
        resultado_lido = cursor.fetchone()
        total = resultado_total[0]
        total_lido = resultado_lido[0]
        total_lido += lido
        if total_lido  > total:
            await ctx.send("❗ Cuidado, você ultrapassou o número de páginas..")
        else:
            pag = "UPDATE livros SET paginas_lidas = paginas_lidas + ? WHERE user_id = ? AND titulo = ?"
            cursor.execute(pag,(lido,user_id,titulo_norm))
            db.commit()
            await ctx.send(f"📖 **Registrado! +{lido} páginas para {titulo.title()}.**")
            rank.xp_up(user_id, lido)
            nivel_novo = rank.rankup(user_id)
            if nivel_novo is True:
                await ctx.send(f'**🎉 Parabéns {ctx.author.display_name}! Você subiu de nível!**')
    else:
        await ctx.send(f"🚨 Vish, o livro que você tentou adicionar páginas não existe na sua estante!")

@bot.command()
async def estante(ctx):
    user_id = ctx.author.id
    cursor.execute("SELECT titulo,paginas_lidas,paginas_totais FROM livros WHERE user_id = ?",(user_id,))
    file = profile.user_bg(user_id)
    livros = cursor.fetchall()
    msg_emb = discord.Embed()
    msg_emb.title = f" 📚 Estante Virtual de  {ctx.author.display_name}"
    msg_emb.description = "**• 📦 Acompanhe seu progresso na biblioteca real!**"
    msg_emb.colour = 0x000000
    msg_emb.set_thumbnail(url=ctx.author.display_avatar.url)
    msg_emb.set_image(url=file)
    if not livros:
        return await ctx.send("❗**Sua estante está vazia! Tente registrar um livro primeiro..**")
    else:
        for c in range(len(livros)):
            msg_emb.add_field(name=str(f'📍 ❝ {livros[c][0]} ❞').replace("'",'').title(),inline=False,value=f'➤ *Páginas Totais:* {str(livros[c][2])}\n ➤ *Paginas Lidas:* {str(livros[c][1])}')
    return await ctx.send(embed=msg_emb)

@bot.command()
async def perfil(ctx):
    user_id = ctx.author.id
    user_icon = ctx.author.avatar.url
    lvl = rank.user_rank(user_id)
    xp = rank.user_xp(user_id)
    file = profile.user_pf(user_id)
    prof_emb = discord.Embed()
    prof_emb.title = f"Perfil de {ctx.author.display_name}"
    prof_emb.colour = 0x000000
    prof_emb.description = f"📚 **Bem-vindo à sua estante, {ctx.author.display_name}!**"

    prof_emb.add_field(name="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",value="",inline=False)
    prof_emb.add_field(name='•📋 | Usuário:',value=f'↪︎{ctx.author.mention}',inline=True)
    if lvl is not None:
        prof_emb.add_field(name='• 🏆 | Rank:',value=f'↪︎ Nível: {lvl[0]}',inline=True)
        prof_emb.add_field(name='• ⌛ | TotalXP:', value=f'↪︎ XP: {xp[0]}')
    else:
        prof_emb.add_field(name='• 🏆 | Rank:', value=f'↪︎ Nível: {0}', inline=True)
        prof_emb.add_field(name='• ⌛ | TotalXP:',value=f'↪︎ XP: {0}')
    prof_emb.set_thumbnail(url=user_icon)
    prof_emb.set_image(url=file)
    await ctx.send(embed=prof_emb)

@bot.command()
async def mudar_bg(ctx,link:str):
    user_id = ctx.author.id
    profile.save_bg(user_id,link)
    await ctx.send("📎 **Imagem de fundo da Biblioteca alterada com sucesso!**")

@bot.command()
async def mudar_pf(ctx,link:str):
    user_id = ctx.author.id
    profile.save_pf(user_id,link)
    await ctx.send("📎 **Imagem de fundo do perfil alterada com sucesso!**")

@bot.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="📚 | Guia de Comandos da Estante",
        description="Aqui estão os comandos disponíveis para organizar sua leitura:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="📖 | Gerenciar Leitura",
        value=(
            "`!registrar_livro` - Adiciona um novo livro à sua estante\n (Paginas-totais e Titulo)\n"
            "`!ler` - Registra o progresso de páginas lidas.\n (Paginas-lidas e Titulo)\n"
            "`!apagar_livro` - Remove um livro da sua biblioteca."
        ),
        inline=False
    )
    # Seção de Customização
    embed.add_field(
        name="🎨 | Customização",
        value=(
            "`!mudar_bg` - Altera a imagem de fundo da sua estante.\n"
            "`!mudar_pf` - Altera a sua imagem de perfil."
        ),
        inline=False
    )
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
"""Insira o Token do bot aqui.."""
bot.run("")