# CRDT servers

A ideia é construir, baseado no servidor de broadcast, um servidor de CRDT.

Um tipo de dados replicado sem conflito [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) é uma estrutura de dados que é replicada em vários computadores em uma rede com as seguintes características:
- O aplicativo pode atualizar qualquer réplica independentemente, simultaneamente e sem coordenação com outras réplicas.
- Um algoritmo resolve automaticamente quaisquer inconsistências que possam ocorrer; e 
- Embora as réplicas possam ter estados diferentes em qualquer ponto específico no tempo, é garantido que convergirão eventualmente.

## G-set (gset.py)

Com G-set queremos criar um conjunto de elementos compartilhados entre diversos servidore e este conjunto está em constante crescimento. 
Os clientes emitem:
- solicitações de adição (adiciona um novo elemento) ou 
- solicitações de leitura (obtem todos os elementos).

Se nosso conjunto de elementos for razoavelmente pequeno, de modo que caiba em uma única mensagem, podemos fazer uma atualização mais agressiva. Em vez de tentar descobrir quem precisa de quais elementos e quando, poderíamos simplesmente enviar todo o nosso conjunto para nossos vizinhos periodicamente. Entregaremos os mesmos elementos várias vezes, mas tudo bem: a união de conjuntos é idempotente.

## Contadores (counters.py)

Esta variação é um contador consistente que suporta incrementos e decrementos.
Os clientes emitem operações de adição para incrementar o valor do contador e operações de leitura para obter o valor do contador atual.
Maelstrom espera que o valor final do contador seja igual à soma de todas as adições (levando em consideração que alguns incrementos podem ou não ter acontecido).

O contador PN usa dois contadores: um para incrementos e outro para decréscimos.
Precisamos destes dois contadores para resolver um problema quando vamos realizar a união de dois contadores.
A função de adição adiciona deltas positivos e negativos da mesma maneira. 
Por exemplo, se começarmos com o mapa do contador {"n1" 2} e chamarmos .add("n1", -5}), o mapa resultante será {"n1" -3}.
Mas o que aconteceria se fundíssemos esses valores? Escolheríamos o valor máximo para n1, que seria 2, não -3. O incremento negativo é efetivamente perdido.


# Preparação

Utilizamos o arquivo node.py de Broadcast. Portanto, precisamos copia-lo para o diretório local.

```
cp 02-Broadcast/node.py 03-crdts/

```
