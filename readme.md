# Estudo de localização no espaço

### Estudo de localização usando libs do python3 
Para preparar o ambiente virtual no windows com powershell
```sh
python -m venv venv
.\venv\Scripts\activate.ps1
pip3 install -r .\requirements.txt
```

O arquivo triangulation possui um microsservico em flask que recebe um (x, y) por post no endpoint /locate para definir onde está esse ponto no plano da area