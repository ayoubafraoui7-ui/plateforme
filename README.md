# Diabetes Data Analytics

Interactive Streamlit dashboard built on a SQLite star-schema data warehouse
of hospital diabetes encounters (Kaggle `diabetesdata`, 291 hospitalizations,
202 patients, Jan 2022 – Dec 2023).

Pages: overview, hospital analysis, data exploration, data quality,
database structure, administration (password-protected form to add records).

## Run locally

```bash
pip install -r requirements.txt

# Linux / macOS
export ADMIN_PASSWORD="choose-a-password"
# Windows (PowerShell)
# $env:ADMIN_PASSWORD="choose-a-password"

streamlit run app.py
```

The admin page stays locked until `ADMIN_PASSWORD` is set
(optional: `ADMIN_USER`, default `admin`).

## Files

- `app.py` : Streamlit application
- `dwh_diabete.db` : SQLite data warehouse (1 fact table, 4 dimensions)
- `requirements.txt` : Python dependencies

Authors: Ayoub Afraoui, supervised by Pr. Mohammed Ait Daoud.
Presented at ICAIS'26, Casablanca.
