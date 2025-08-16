import os, json
from fastapi import FastAPI, Response, Request
from cryptography.fernet import Fernet

app = FastAPI()
fernet = Fernet(os.environ["FERNET_KEY"].encode())

@app.post("/ask")
async def ask(request: Request):
    # recebe corpo cifrado (bytes base64 Fernet)
    enc = await request.body()
    data = json.loads(fernet.decrypt(enc).decode())

    qid = data["qid"]
    question = data["question"]
    options = data["options"]

    # mostra ao usuário local e lê uma opção 1..5
    print("\n=== Nova pergunta recebida ===")
    print(f"Q{qid}: {question}")
    for i, opt in enumerate(options, 1):
        print(f"{i}) {opt}")
    while True:
        try:
            ans = int(input("Sua resposta (1-5): ").strip())
            if 1 <= ans <= 5:
                break
        except: pass
        print("Valor inválido, tente novamente (1–5).")

    resp = json.dumps({"qid": qid, "answer": ans}).encode()
    return Response(content=fernet.encrypt(resp), media_type="application/octet-stream")