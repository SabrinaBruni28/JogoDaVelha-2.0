criar_ambiente:
	python3 -m venv .venv

salvar_bibliotecas:
	@pip freeze > requirements.txt

instalar_bibliotecas:
	@pip install -r requirements.txt
	@python3 -m pip install --upgrade pip

run:
	@echo "Iniciando Jogo da Velha"
	@PYTHONDONTWRITEBYTECODE=1 python3 jogo_da_velha.py