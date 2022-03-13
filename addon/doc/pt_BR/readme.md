# YoutubeChanelManager.
[Gerardo Késsler] (http://gera.ar)

Este complemento permite gerir os canais favoritos da plataforma YouTube com atalhos de teclado e uma interface invisível e simples.

## atalhos de complemento

* NVDA + I Grego; Ativa e desativa a interface invisível

## Atalhos disponíveis na interface invisível

* escape; Fecha a interface virtual e volta ao teclado com a sua função padrão.
* Seta direita; move-se para o próximo canal.
* Seta esquerda; move-se para o canal anterior.
* Seta para baixo; move-se para o próximo vídeo do canal com o foco.
* Seta para cima; move-se para o vídeo anterior do canal com o foco.
* Início; move-se para o primeiro vídeo do canal com o foco.
* Fim; Verifica a posição, o nome do canal e o número de visualizações do vídeo.
* n; Abre a caixa de diálogo para adicionar um novo canal.
* o; Abre o link do vídeo no navegador padrão.
R; Abre o link de áudio num web player personalizado.
* c; Copia o link de vídeo para a área de transferência.
D; Obtém os dados do vídeo e mostra-os numa janela do NVDA
* b; Ativa a caixa de diálogo de pesquisa na base de dados.
* Controlo + B; Ativa a caixa de diálogo de pesquisa geral.
* F5; Pesquisa se há novos vídeos no canal com o foco.
* S; Ativa a janela de Configuração do canal com o foco.
G; Ativa a janela de Opções globais.
* Apagar; Remove o canal com o foco e, na janela de Resultados, exclui a coluna e retorna à lista de canais.
* Controlo + SHIFT + DELETE; Elimina a base de dados.
* F1; Ativa a ajuda dos comandos.

### Adicionar canais.

Para adicionar um novo canal à base de dados, só precisa abrir a interface virtual com o atalho para essa ação, por padrão; NVDA + I GREGO. E pressionar a letra n.
A janela apresenta 2 campos. Um nome de canal e o URL dele. Neste último caso, o complemento permite a entrada dos seguintes formatos de URL:

* Link de um vídeo, que geralmente tem o seguinte formato:

    https://www.youtube.com/watch?v=iddelvideo.

* Link de um canal

    https://www.youtube.com/channel/iddelcanal.

Pelo que uma forma de o conseguir é abrindo algum víideo na página do Youtube a través do navegador, pressionar alt e a letra d para abrir a barra de direções, e copiar a URL com control + c, a qual já estará selecionada, por padrão.
Os canais também podem ser adicionados a partir da lista de resultados globais. Para isso, basta fazer a busca, posicionar o cursor sobre o vídeo do canal para ser adicionado e pressionar a tecla N.
Isso ativará a caixa de diálogo para inserir os dados do canal, que serão concluídos automaticamente com o link e o nome retirado do YouTube.

### atualizador automático:

O complemento permite marcar canais como favoritos e ativar a verificação de notícias com um intervalo de tempo estipulado.
Para marcar ou desmarcar um canal como favorito:

* Ativar a interface virtual com o comando atribuído, por padrão, NVDA + I Grego.
* Selecionar o canal desejado com as setas esquerda ou direita.
* Ativar a janela Configuração do canal com a letra S.
* Marcar a caixa correspondente e ativar o botão para guardar a configuração.

A verificação de notícias nos canais favoritos encontra-se desativada por padrão. Para modificá-la, precisa de efetuar as seguintes etapas:

* Ativar a interface virtual com o comando atribuído, por padrão, NVDA + I Grego.
* Ativar a janela de configuração global com a letra g.
* Tabular para a lista de opções e selecionar, com as setas para cima e para baixo, o intervalo desejado.
* Pressionar o botão para guardar as configurações.

Quando encontrar notícias, o plug-in emitirá um som durante a atualização e uma mensagem no final.

### Procurar por vídeos na base de dados:

O complemento permite pesquisar por palavras-chave entre os vídeos dos canais já adicionados à base de dados.

* Ativar a interface virtual com o comando atribuído, por padrão, NVDA + I Grego.
* Ativar a janela de pesquisa com a letra b.
* Escrever uma palavra ou frase de referência.
* Pressionar ENTER ou o botão Iniciar pesquisa.

Se nenhum resultado for encontrado, isso será notificado por meio de uma mensagem e a interface virtual não será modificada.
No caso de encontrar vídeos que correspondem aos dados inseridos, é notificado por meio de uma mensagem e a interface de resultados é ativada.
Para navegar, podem fazê-lo com setas para cima e para baixo. Os mesmos comandos estão disponíveis como na interface do canal; R para o web player personalizado, ou para abrir no navegador, etcetera.
Para retornar à interface do canal, precisa pressionar a tecla Excluir na interface de resultados, que irá excluir essa coluna e retornará a lista de canais e vídeos.

### Pesquisa Global:

Para executar uma pesquisa global fora da base de dados, deve fazer o seguinte:

* Ativar a interface virtual com o comando atribuído, por padrão, NVDA + I Grego.
* Ativar a janela de pesquisa com o atalho controlo+b.
* Escrever uma palavra de referência ou frase e selecionar a quantidade de resultados a serem mostrados.
* Pressionar o botão Iniciar pesquisa.

Se nenhum resultado for encontrado, será notificado através de uma mensagem.
Quando os resultados são encontrados, estes são adicionados à lista principal, que podemos navegar com setas para cima e para baixo.
Aqui também temos os mesmos atalhos que na busca na base de dados. Ou para abrir no navegador, r para o web player, C para copiar o link, etc.
Se algum dos vídeos estiver num canal que deseja adicionar à base de dados, pressionar a letra n nesta lista ativará a caixa de diálogo Novo canal com os campos Nome e URL e concluirá. Esses campos podem ser editados se preferirem.
Como nas pesquisas na base de dados, para voltar à lista de canais, só precisa pressionar Excluir para excluir os resultados e retornar à interface do canal.

### Tradutores

Rémy Ruiz, para francês.
wafiqtaher (árabe)
Umut KORKMAZ (turco)

Equipa portuguesa do NVDA: Ângelo Abrantes e Rui Fontes
(10-03-2022)
