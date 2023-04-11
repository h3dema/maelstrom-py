# Um servidor de echo simples

Vamos ver como escrever um servidor de eco básico em python, usando o Maelstrom como uma ferramenta de teste.
Um servidor de echo aceita mensagens de clientes com algum payload (mensagem) e responde a esse cliente com o mesmo payload.
Vamos seguir os mesmos passos mostrados em [A Simple Echo Server](https://github.com/jepsen-io/maelstrom/blob/main/doc/02-echo/index.md).


- echo_minimal.py
    + Contem uma primeira versão (não funcional) do servidor Echo. Permite conhecer as funcionalidades básicas necessárias para o funcionamento do servidor

- echo.py
    + Versão final do servidor Echo com os dois handlers necessários para funcionamento do servidor: "init" e "echo".

> No cabeçalho de cada modulo python (acima), você irá encontrar o comando para testa-lo com o Maelstrom.