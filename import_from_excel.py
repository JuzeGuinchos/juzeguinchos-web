import os, sys, pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

def norm(v):
    if pd.isna(v):
        return None
    if isinstance(v, float) and pd.isna(v):
        return None
    if isinstance(v, str):
        v = v.strip()
        return v if v else None
    return v

def import_clientes(engine, path):
    if not os.path.exists(path):
        print("clientes.xlsx não encontrado:", path); return
    df = pd.read_excel(path)
    df.columns = [c.strip().lower() for c in df.columns]
    rename = {"razao social":"razao_social","nome fantasia":"nome_fantasia"}
    df.rename(columns=rename, inplace=True)
    cols = ["cnpj","razao_social","nome_fantasia","cep","logradouro","numero","complemento","bairro","municipio","uf","telefone","email","inscricao_estadual","observacoes"]
    for c in cols:
        if c not in df.columns: df[c] = None
    df = df[cols].copy().applymap(norm)
    df.to_sql("cliente", engine, if_exists="append", index=False)
    print(f"Importados {len(df)} clientes.")

def import_veiculos(engine, path):
    if not os.path.exists(path):
        print("veiculos.xlsx não encontrado:", path); return
    df = pd.read_excel(path)
    df.columns = [c.strip().lower() for c in df.columns]
    cols = ["placa","modelo","marca","ano","renavam","chassi","proprietario","observacoes"]
    for c in cols:
        if c not in df.columns: df[c] = None
    df = df[cols].copy().applymap(norm)
    df.to_sql("veiculo", engine, if_exists="append", index=False)
    print(f"Importados {len(df)} veículos.")

def import_lancamentos(engine, comp_dir):
    if not os.path.isdir(comp_dir):
        print("Pasta de competências não encontrada:", comp_dir); return
    total = 0
    for fname in os.listdir(comp_dir):
        if not fname.lower().endswith(".xlsx"): continue
        if not fname.lower().startswith("lancamentos_"): continue
        path = os.path.join(comp_dir, fname)
        df = pd.read_excel(path)
        cols = ["id","data","tipo","cliente","cnpj","veiculo","placa","descricao","categoria","valor","origem","destino","cidade_despesa"]
        for c in cols:
            if c not in df.columns: df[c] = None
        df = df[cols]
        def parse_data(x):
            try:
                if pd.isna(x) or x == "": return None
                if isinstance(x, str): return pd.to_datetime(x).date()
                return pd.to_datetime(x).date()
            except Exception:
                return None
        df["data"] = df["data"].apply(parse_data)
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0).round(2)
        for c in ["tipo","cliente","cnpj","veiculo","placa","descricao","categoria","origem","destino","cidade_despesa"]:
            df[c] = df[c].apply(lambda v: None if (isinstance(v,float) and pd.isna(v)) else (v.strip() if isinstance(v,str) else v))
        df = df.drop(columns=["id"])
        df.to_sql("lancamento", engine, if_exists="append", index=False)
        total += len(df)
    print(f"Importados {total} lançamentos.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python import_from_excel.py <DATABASE_URL> <pasta_planilhas> <pasta_competencias>")
        sys.exit(1)
    db_url, planilhas, competencias = sys.argv[1], sys.argv[2], sys.argv[3]
    engine = create_engine(db_url)
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS cliente (
            id SERIAL PRIMARY KEY,
            cnpj VARCHAR(32),
            razao_social VARCHAR(255),
            nome_fantasia VARCHAR(255),
            cep VARCHAR(32),
            logradouro VARCHAR(255),
            numero VARCHAR(64),
            complemento VARCHAR(255),
            bairro VARCHAR(255),
            municipio VARCHAR(255),
            uf VARCHAR(8),
            telefone VARCHAR(64),
            email VARCHAR(255),
            inscricao_estadual VARCHAR(64),
            observacoes TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_cliente_cnpj ON cliente(cnpj);
        CREATE TABLE IF NOT EXISTS veiculo (
            id SERIAL PRIMARY KEY,
            placa VARCHAR(32),
            modelo VARCHAR(128),
            marca VARCHAR(128),
            ano VARCHAR(16),
            renavam VARCHAR(64),
            chassi VARCHAR(64),
            proprietario VARCHAR(128),
            observacoes TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_veiculo_placa ON veiculo(placa);
        CREATE TABLE IF NOT EXISTS lancamento (
            id SERIAL PRIMARY KEY,
            data DATE,
            tipo VARCHAR(32),
            cliente VARCHAR(255),
            cnpj VARCHAR(32),
            veiculo VARCHAR(255),
            placa VARCHAR(32),
            descricao TEXT,
            categoria VARCHAR(128),
            valor NUMERIC(14,2),
            origem VARCHAR(255),
            destino VARCHAR(255),
            cidade_despesa VARCHAR(255)
        );
        """))
    import_clientes(engine, os.path.join(planilhas, "clientes.xlsx"))
    import_veiculos(engine, os.path.join(planilhas, "veiculos.xlsx"))
    import_lancamentos(engine, competencias)
    print("Pronto!")
