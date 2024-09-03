import requests
import datetime
import json

# Soru ve cevapları tutacak listeyi başta tanımlıyoruz
konusma_gecmisi = []

def bot(soru):
    url = "http://localhost:11434/api/generate"  # Ollama'nın varsayılan local API endpointi
    payload = {
        "prompt": soru,
        "model": "llama3:latest",  # Model adını buraya yazdık
        "temperature": 0.7
    }

    response = requests.post(url, json=payload)

    try:
        # Split the response content by newline characters
        json_objects = response.content.decode().split('\n')
        responses = []

        # Parse each JSON object and collect the 'response' fields
        for obj in json_objects:
            if obj.strip():  # Skip empty lines
                data = json.loads(obj)
                responses.append(data['response'])

        # Concatenate all responses
        cevap = ''.join(responses).strip()
    except json.JSONDecodeError:
        print("Response content is not valid JSON:", response.content)
        cevap = "An error occurred while processing the response."

    return cevap

while True:
    soru = input("Sorunuzu yazın: ")
    if soru.lower() in ["çık", "exit", "quit"]:
        break

    cevap = bot(soru)
    print(f"Cevap: {cevap}")

    # Soru ve cevabı listeye ekle
    konusma_gecmisi.append(f"Soru: {soru}\nCevap: {cevap}\n")

# Konuşma oturumu bittiğinde dosyaya yaz
tarih_saat = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dosya_adi = f"konusma_{tarih_saat}.txt"

with open(dosya_adi, "w") as file:
    for kayit in konusma_gecmisi:
        file.write(kayit + "\n")

print(f"Konuşma geçmişi '{dosya_adi}' dosyasına kaydedildi.")