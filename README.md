# Juzé Guinchos Web (Flask + Postgres)

Este projeto transforma seu app local em uma versão web com autenticação e banco de dados.
Pilha: Flask, SQLAlchemy, Flask-Login, Postgres. Pronto para deploy no Render (free).

## 1) Rodar local (opcional para testar)
1. Python 3.12+ instalado
2. `python -m venv .venv && .venv\Scripts\activate` (Windows) ou `source .venv/bin/activate` (mac/linux)
3. `pip install -r requirements.txt`
4. Crie `.env` copiando de `.env.example` (opcional; por padrão usa SQLite local)
5. `python run.py` e acesse http://localhost:5000

### Criar o primeiro usuário admin
Após subir localmente (ou em produção), crie o admin:
```
curl -X POST https://SEU_HOST/auth/first-admin -d "username=admin&password=SUA_SENHA"
```
(Depois remova/desabilite essa rota, se preferir, comentando no arquivo `auth.py`).

## 2) Deploy no Render (plano free)
1. Suba este projeto em um repositório **GitHub** novo.
2. No site do **Render**, crie novo projeto e selecione seu repositório.
3. O arquivo `render.yaml` já cria:
   - um **Web Service** (Flask com Gunicorn)
   - um **Banco Postgres** (free) e injeta `DATABASE_URL` no Web Service
4. Finalizado o deploy, o Render dará uma URL (https).

## 3) Importar seus dados existentes (Excel)
Seus dados do app atual ficam em `dados/planilhas/` e `dados/planilhas/competencias/`.
Você pode importar **direto para o Postgres** do Render:

**Opção A — Rodando local apontando para o banco do Render**
- Verifique a variável `DATABASE_URL` no dashboard do Render (Copiar string de conexão).
- Baixe/copiar suas planilhas do zip para uma pasta local (ex.: `./dados/planilhas` e `./dados/planilhas/competencias`).
- Rode:
```
pip install -r requirements.txt
python import_from_excel.py "postgresql://USER:PASS@HOST:5432/DB" ./dados/planilhas ./dados/planilhas/competencias
```

**Opção B — Rodando pela própria instância (shell)**
- No Render, abra um Shell do serviço web (se disponível) e rode o mesmo comando, após subir os arquivos (via git).

## 4) Uso
- Acesse `/auth/login` para entrar.
- Dashboard mostra totais e últimos lançamentos.
- CRUDs simples para **Clientes**, **Veículos** e **Lançamentos**.

## Notas
- Estrutura dos campos segue o que existia nas suas planilhas (COLS_* do app antigo).
- Ajustes de telas/validações podem ser evoluídos com o tempo.
- Para performance e uploads grandes, considere planos pagos.
