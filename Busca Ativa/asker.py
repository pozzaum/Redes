import os, json, asyncio, aiohttp, sys, collections
from cryptography.fernet import Fernet
from collections import Counter

FERNET_KEY = os.environ["FERNET_KEY"].encode()
fernet = Fernet(FERNET_KEY)

async def ask_node(session, url, payload, timeout=15):
    enc = fernet.encrypt(json.dumps(payload).encode())
    try:
        async with session.post(f"{url}/ask", data=enc, timeout=timeout) as r:
            enc_resp = await r.read()
            data = json.loads(fernet.decrypt(enc_resp).decode())
            return url, data["answer"]
    except Exception:
        return url, None

async def main(urls):
    payload = {
        "qid": 1,
        "question": "Qual é o número atômico do Oxigênio?",
        "options": ["6", "7", "8", "9", "10"]
    }
    async with aiohttp.ClientSession() as session:
        tasks = [ask_node(session, u, payload) for u in urls]
        results = await asyncio.gather(*tasks)

    answers = []
    print("\n--- Respostas recebidas ---")
    for url, ans in results:
        print(f"{url}: {ans if ans is not None else 'sem resposta'}")
        if ans is not None:
            answers.append(ans)

    if not answers:
        print("Nenhuma resposta válida. Sem consenso.")
        return

    ctr = Counter(answers)
    most_common = ctr.most_common()
    top_ans, top_count = most_common[0]

    tied = [a for a, c in most_common if c == top_count]

    if len(tied) > 1:
        print("\n--- Resultado ---")
        print("Sem consenso (empate).")
        print(f"Distribuição: {dict(ctr)}")
        return

    if top_count <= len(answers) // 2:
        print("\n--- Resultado ---")
        print("Sem consenso (sem maioria absoluta).")
        print(f"Distribuição: {dict(ctr)}")
        return

    print("\n--- Resultado ---")
    print(f"Vencedor: alternativa {top_ans} ({top_count} votos).")
    print(f"Distribuição: {dict(ctr)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python asker.py <url_no_1> <url_no_2> ...")
        sys.exit(1)
    asyncio.run(main(sys.argv[1:]))
