# maelstrom-py

Apresentamos aqui os exemplos em python para o projeto [maelstrom](https://github.com/jepsen-io/maelstrom).
Maelstrom é um ambiente que você pode utilizar para aprender sistemas distribuídos escrevendo o seu próprio sistema.
Ele usa a biblioteca de testes __Jepsen__ para testar implementações de sistemas distribuídos.
Maelstrom fornece testes padronizados e permite que você aprenda escrevendo implementações que esses conjuntos de teste.

Maelstrom utiliza um protocolo JSON simples via STDIN e STDOUT.
Os usuários escrevem servidores em qualquer linguagem capaz de manipular estes dispositivos.
Ele executa os servidores desenvolvidos, envia solicitações, roteia mensagens por meio de uma rede simulada e verifica se os clientes observam o comportamento esperado.

Maelstrom fornece os seguintes servidores.
- Echo
- Broadcast
- CRDTs
- Datomic
- [Raft](https://github.com/jepsen-io/maelstrom/blob/main/demo/python/raft.py)

Raft é fornecido no repositório jepsen-io como exemplo.
Assim aqui apresentaremos os outros quatro.


## Instalar modulos

As linhas abaixo mostram como criar um ambiente de desenvolvimento separado da sua instalação principal usando `venv` no linux.
Utilizamos __pip__ para instalar os módulos necessários.
No Ubuntu os comandos são:

```
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt
```


## Preparar o ambiente

O Maelstrom utiliza alguns pacotes para funcionar. No Ubuntu basta:

```
sudo apt install openjdk-17-jdk
sudo apt install graphviz
sudo apt install gnuplot
```

Você precisa baixar o tarball mais recente (maelstrom.tar.bz2, não o código-fonte!) do GitHub.
Descompacte-o e execute ./maelstrom <args> para iniciar o Maelstrom.

```
wget https://github.com/jepsen-io/maelstrom/releases/download/v0.2.3/maelstrom.tar.bz2
tar xvjf maelstrom.tar.bz2
cd maelstrom
```