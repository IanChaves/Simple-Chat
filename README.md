# Atividade de Programação - Chat Simples - Sistema Distribuído

## Ian Marcos da Cruz Chaves - Matrícula: 201802684

Este é um projeto de chat simples em Python, desenvolvido como parte de uma atividade de programação no contexto de um sistema distribuído. O projeto é composto por um servidor de chat e clientes de chat que se comunicam entre si.

## Funcionamento do Código

### `chatserver.py`

Este arquivo implementa o servidor de chat. Ele aceita conexões de clientes, recebe mensagens dos clientes remetentes e retransmite essas mensagens para os clientes destinatários. Algumas melhorias implementadas são:

1. Uso de multithreading para melhorar a escalabilidade: O servidor aceita conexões de clientes em threads separadas, permitindo que múltiplos clientes se conectem e comuniquem simultaneamente.

2. Suporte a múltiplos usuários com cadastro dinâmico: O servidor mantém um registro dinâmico de usuários e seus endereços IP e portas, permitindo que os clientes se registrem e se comuniquem entre si.

### `chatclient.py`

Este arquivo implementa o cliente de chat. Ele se comunica com o servidor para enviar e receber mensagens. Algumas melhorias implementadas são:

1. Uso de multithreading para recepção de mensagens: O cliente inicia uma thread de recebimento de mensagens para que possa continuar enviando mensagens enquanto recebe mensagens de outros clientes.

2. Interação do usuário: O cliente solicita ao usuário que insira um destinatário e uma mensagem, envia essa mensagem ao servidor e aguarda uma confirmação.

### `const.py`

Este arquivo contém constantes como o endereço do servidor de chat e o registro de usuários com seus respectivos endereços IP e portas.

## Exemplo de Uso

1. Execute o servidor de chat:
   ```bash
   python chatserver.py
2. Execute um ou vários clientes de chat:
   ```bash
   python chatclient.py Alice
   python chatclient.py Bob
## Considerações Finais
Este projeto é uma implementação simples de um sistema de chat distribuído em Python. Ele serve como uma introdução aos conceitos de comunicação entre processos e uso de multithreading em sistemas distribuídos.

#Nota: 
Certifique-se de que os endereços IP e portas estejam configurados corretamente no arquivo const.py para que o servidor e os clientes possam se comunicar adequadamente.
