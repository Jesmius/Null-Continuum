# Null-Continnum
Lucas Fernandes Alvarenga
Matrícula: 2210601


# Disclaimers:
    - (1) - Eu não fiz o estilo do site, eu pedi para o Claude fazer, já que minhas tentativas de fazer um estilo bonito foram terríveis
    - (2) - Pelo menos no VS Code, o arquivo "character_detail.html" aparenta ter um erro, mas é so o VS Code reclamando da sintaxe do Django, o site roda normalmente 

# O que foi desenvolvido:
    - Há 2 tipos de usuários no Site, os Jogadores e os Game Masters, para os jogadores, foi implementado um sistema de criação e gerência de personagens para o RPG de Mesa em questão, e para os Game Masters, há o sistema de criação e gerência de Campanhas, onde o GM pode convidar jogadores para participar, e gerenciar os personagens que fazem parte da campanha.

# O que não foi desenvolvido:
    - A gerência de usuários não foi feita completamente, não consegui implementar a tempo o sistema de recuperação de senha que foi visto durante as aulas.
    - Na ideia inicial, os Game Masters teriam um "Initiative Tracker", onde eles poderiam gerenciar a ordem que os jogadores e os diversos inimigos iriam agir durante o combate, porém, o escopo da criação dos personagens foi maior do que o esperado, e não consegui implementar esse sistema a tempo.
    

# O que Funciona:
    - A criação de personagens funciona por completo, incluindo distribuição de atributos, seleção de skills, background, traits, feats de combate e de operações, e feats não-lineares.
    O sistema de Rank Up funciona, permitindo que o jogador melhore skills e escolha novos feats ao subir de rank (com liberação controlada pelo GM).
    - A ficha de personagem exibe todos os valores calculados (HP, PD, Defesa, Capacidade de Carga etc.) e permite edição de campos de sessão.
    Companheiros e Veículos podem ser adicionados e gerenciados diretamente na ficha, com HP e Strain rastreados via botões.
    - O sistema de Campanhas funciona: GMs podem criar campanhas, convidar jogadores pelo nome de usuário, e os jogadores podem submeter personagens para a campanha.

# O que não Funciona:
    - Caso dê algum erro durante a criação de certos formulários na criação de personagem (não escolheu o número certo de skills, ou não usou todos os pontos de atributo por exemplo), certos campos do Form devem ser colocados de novo (principalmente as skills)
    - GMs não são capazes de editar TODOS os aspectos da ficha dos personagens
    - Idealmente cada bacground teria uma lista de Skills pré-definida, porém eu mudei isso pois estava muito complexo de implementar, porém, os Backgrounds ainda tem essa lista definida internamente no arquivo.py
    - É possível "quebrar" a ficha com muito rank ups, porém como eles são definidos pelo GM, não acho que isso é um grande problema
    

# Manual do Usuário:

## Como rodar o projeto:
    1. Instale as dependências: pip install -r requirements.txt
    2. Entre na pasta do projeto: cd NullContinuum
    3. Rode as migrações: python manage.py migrate
    4. Popule o banco de dados com as regras: python manage.py sync_rulebook
    5. Crie um superusuário se quiser acessar o admin: python manage.py createsuperuser
    6. Inicie o servidor: python manage.py runserver
    7. Acesse http://127.0.0.1:8000/

## Criando um usuário:
    Ao acessar o site pela primeira vez, clique em "Registrar".
    Escolha um nome de usuário, senha, e selecione seu tipo de conta:
        - Jogador: para criar e gerenciar personagens
        - Game Master: para criar e gerenciar campanhas

---

# Manual do Jogador:

## Criando um Personagem:
    A criação de personagem é dividida em etapas. Cada etapa deve ser completada antes de avançar para a próxima.

    Etapa 1 — Informações Básicas:
        - Informe o nome do personagem e escolha o Background dele.
        - O Background concede um Trait de Background pré-definido.

    Etapa 2 — Atributos:
        - Distribua 10 pontos entre os 6 atributos: AGI, FOR, INS, PRE, STA, INT.
        - Cada atributo começa em 1 e pode ser aumentado até 3.
        - Todos os pontos devem ser gastos antes de avançar.

    Etapa 3 — Skills:
        - Escolha exatamente 4 skills para começar como "Trained" (T).
        - As skills partem de Untrained (U) → Trained (T) → Proficient (P) → Expert (E).

    Etapa 4 — Traits:
        - Você começa com 10 Trait Points (TP).
        - Traits positivos custam TP; traits negativos fornecem TP adicional.
        - Os TP devem ser zerados exatamente ao confirmar (não pode sobrar nem faltar).

    Etapa 5 — Feats de Combate:
        - Gaste seus Combat Feat Points escolhendo feats nas árvores disponíveis.
        - Alguns feats dependem de pré-requisitos na mesma árvore.

    Etapa 6 — Feats de Operações:
        - Gaste seus Operations Feat Points da mesma forma que os de Combate.

    Etapa 7 — Feats Não-Lineares (opcional):
        - Disponível apenas se o personagem possuir NL Rank > 0 (concedido por Traits ou pelo GM).
        - Escolha feats nas árvores NL disponíveis.

## Gerenciando o Personagem:
    - Na ficha do personagem, você pode rastrear HP atual, usar botões de dano/cura, e atualizar Armor/Shield.
    - Companheiros e Veículos podem ser adicionados pela ficha e têm seus próprios controles de HP e Strain.
    - O botão de Rank Up aparece somente quando o GM liberar para o seu personagem.

## Rank Up:
    - Ao subir de Rank, você pode melhorar um número de Skills e escolher novos Feats (Combat, Ops e/ou NL).
    - O número de upgrades disponíveis depende do Rank atual (veja a tabela na tela de Rank Up).
    - Após confirmar o Rank Up, o botão desaparece até o GM liberá-lo novamente.

## Participando de uma Campanha:
    - Se um GM convidou você pelo seu nome de usuário, a campanha aparecerá na sua tela inicial.
    - Acesse a campanha e clique em "Submeter Personagem" para enviar um personagem ao GM.
    - O GM poderá então visualizar e editar a ficha desse personagem.

---

# Manual do Game Master:

## Criando uma Campanha:
    1. Na tela inicial, clique em "Campanhas" e depois em "Nova Campanha".
    2. Dê um nome à campanha e confirme.

## Convidando Jogadores:
    1. Dentro da campanha, use o campo "Convidar Jogador" para adicionar um jogador pelo nome de usuário exato.
    2. O jogador aparecerá na lista de membros e poderá submeter personagens.
    3. Para remover um membro, clique no botão "Remover" ao lado do nome dele.

## Gerenciando Personagens:
    - Os personagens submetidos pelos jogadores aparecem na coluna direita da tela da campanha.
    - Clique no nome do personagem para abrir a ficha completa.
    - Na ficha, o GM pode editar qualquer campo: atributos, skills, rank, notas etc.
    - Para remover um personagem da campanha, use o botão "Remover" na tela da campanha.

## Liberando Rank Up:
    - Por padrão, nenhum personagem pode subir de Rank.
    - Na tela da campanha, clique em "Liberar LvlUp" ao lado do personagem para permitir que aquele jogador suba de Rank.
    - Após o jogador confirmar o Rank Up, o botão é automaticamente bloqueado novamente.
    - Para revogar a permissão antes do jogador usá-la, clique em "Bloquear LvlUp".
