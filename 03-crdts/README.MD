# CRDT servers

A ideia é construir baseado no servidor de broadcast um servidor de CRDT.

Um tipo de dados replicado sem conflito [CRDT](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) é uma estrutura de dados que é replicada em vários computadores em uma rede com as seguintes características:
- O aplicativo pode atualizar qualquer réplica independentemente, simultaneamente e sem coordenação com outras réplicas.
- Um algoritmo resolve automaticamente quaisquer inconsistências que possam ocorrer; e 
- Embora as réplicas possam ter estados diferentes em qualquer ponto específico no tempo, é garantido que convergirão eventualmente.

## G-set

Com G-set queremos criar um conjunto de elementos compartilhados entre diversos servidore e este conjunto está em constante crescimento. 
Os clientes emitem:
- solicitações de adição (adiciona um novo elemento) ou 
- solicitações de leitura (obtem todos os elementos).

Se nosso conjunto de elementos for razoavelmente pequeno, de modo que caiba em uma única mensagem, podemos fazer uma atualização mais agressiva. Em vez de tentar descobrir quem precisa de quais elementos e quando, poderíamos simplesmente enviar todo o nosso conjunto para nossos vizinhos periodicamente. Entregaremos os mesmos elementos várias vezes, mas tudo bem: a união de conjuntos é idempotente.

## Contadores



# Preparation:

Copiar o arquivo node.py de Broadcast.

```
cp 02-Broadcast/node.py 03-crdts/

```
