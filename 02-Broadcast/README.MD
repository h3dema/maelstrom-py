# Broadcast baseada em gossip

Um sistema de broadcast permite compartilhar uma mensagem com todos os nós daquele segmento derede.
No Maelstrom, podemos criar um sistema de transmissão com uma API simples:

- Uma mensagem de topologia informa ao nó a topologia da rede (opcional): um mapa de nós para vizinhos.
- Uma solicitação de transmissão envia uma mensagem para a rede.
- Uma solicitação de leitura lê todas as mensagens presentes em um único nó.

O Maelstrom verifica se cada mensagem de broadcast chega (eventualmente) a cada nó da rede e pode dizer quanto tempo leva para isso acontecer - bem como quantas mensagens foram necessárias.

A ideia deste bloco de códigos é construirmos um conjunto de sistemas de broadcast.
Construiremos uma abstração reutilizável para servidores de rede (node.py) e veremos como falhas de rede e diferentes estratégias para novas tentativas afetam a entrega de mensagens.

