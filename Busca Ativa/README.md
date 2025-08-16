# Sistema de Votação Distribuída com FastAPI + Fernet

Este projeto implementa uma comunicação simples em rede entre **um solicitante** e **vários nós respondentes** para realizar uma votação.  
O solicitante envia uma **pergunta objetiva** com alternativas numeradas (1 a 5). Cada nó respondente apresenta a pergunta ao usuário local, que digita sua resposta.  
O solicitante coleta as respostas e decide o **resultado pela maioria** (ou "sem consenso" em caso de empate).

---

## 🔗 Comunicação Utilizada

- **Protocolo**: HTTP (`POST /ask`)
- **Bibliotecas**: [FastAPI](https://fastapi.tiangolo.com/) para os nós respondentes, [aiohttp](https://docs.aiohttp.org/) para o solicitante.
- **Segurança**: O corpo da mensagem é **cifrado com Fernet (AES + HMAC)**.  
  - Uma **chave simétrica única** é gerada e compartilhada entre solicitante e respondentes.
  - Assim, mesmo que alguém intercepte os pacotes, não conseguirá ler as informações.

---

## ⚙️ Pré-requisitos

- **Python 3.10+** instalado na VM e no Windows.
- Pacotes necessários:
  ```bash
  pip install fastapi uvicorn aiohttp cryptography


### 🖥️ Passos Rápidos – VM Linux (Nós Respondentes)

- **Gerar a Fernet Key**
    ```
    python3 - <<'PY'
    import node_responder
    print("Tem app?", hasattr(node_responder, "app"))
    PY
    ```

- **Exportar a Fernet Key (igual em todos os terminais)**
  ```bash
  export FERNET_KEY="SUA_CHAVE_AQUI"

- **Rodar múltiplos nós (cada um em um terminal separado)**

    ```
    uvicorn node_responder:app --host 0.0.0.0 --port 8001
    uvicorn node_responder:app --host 0.0.0.0 --port 8002
    uvicorn node_responder:app --host 0.0.0.0 --port 8003
    ```

### 🖥️ Passos Rápidos – Windows (Solicitante via PowerShell)

- **Exportar a mesma Fernet Key usada na VM**
    ```bash
    $env:FERNET_KEY="SUA_CHAVE_AQUI"

- **Rodar o solicitante apontando para o IP da VM**
    ```bash
    python asker.py http://192.168.x.x:8001 http://192.168.x.x:8002 http://192.168.x.x:8003

## ✅ Exemplo de Execução

- **Nos respondentes (VM):**

    ```
    === Nova pergunta recebida ===
    Q1: Qual é o número atômico do Oxigênio?
    1) 6
    2) 7
    3) 8
    4) 9
    5) 10
    Sua resposta (1-5):
    ```

- **No solicitante (Windows):**

    ```
    --- Respostas recebidas ---
    http://192.168.0.10:8001: 3
    http://192.168.0.10:8002: 2
    http://192.168.0.10:8003: 1

    --- Resultado ---
    Sem consenso (empate).
    Distribuição: {3: 1, 2: 1, 1: 1}
    ```