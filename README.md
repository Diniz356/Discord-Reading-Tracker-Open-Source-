# Discord Reading Tracker (Open Source)

Um script em Python modular e de fácil integração para gamificação de leitura em servidores do Discord. Este projeto foi desenvolvido para ser uma base sólida e simples para quem deseja implementar sistemas de XP baseados em progresso de leitura.

## 🚀 Funcionalidades Principais
* **Gerenciamento de Leitura:** Registro de livros, páginas totais e progresso individual.
* **Sistema de Progressão:** Lógica de XP automatizada (1 pág = 10 XP) com sistema de níveis (Level Up a cada 1000 XP).
* **Personalização de Perfil:** Comandos para salvar URLs de imagens e GIFs para customizar a estante virtual e o perfil do usuário.
* **Persistência em SQL:** Integração nativa com SQLite para armazenamento leve e rápido.

## 🏗️ Estrutura do Projeto
O código é dividido em módulos para facilitar a modificação:
* `profile_functions/`: Gerencia o salvamento e busca de imagens de fundo e banners.
* `rank_functions/`: Contém a lógica matemática de XP e a atualização de níveis.
* `main.py`: Ponto de entrada do bot e gerenciamento de comandos.

## ⚙️ Instalação e Customização
1. **Clone o repositório:**
   `git clone https://github.com/seu-usuario/nome-do-repo.git`
2. **Instale as dependências:**
   `pip install -r requirements.txt`
3. **Configure seu Token:**
   Insira o token da sua aplicação no campo indicado em `main.py`.
4. **Altere as Regras:**
   A lógica de XP e Rank pode ser facilmente alterada nos arquivos dentro de `rank_functions/`.

## 🛠️ Tecnologias Utilizadas
* Python
* SQLite3
* Discord.py / Nextcord

## 📄 Licença
Este projeto está sob a licença MIT - sinta-se livre para usar, modificar e distribuir em sua própria aplicação!