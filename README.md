# api_demo

Scripts que leem alarmes de maquina de uma API e gravam no SQL Server.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

- `fetch_machine_alarms.py`: busca os alarmes e imprime o JSON
- `read_machine_alarms.py`: busca os alarmes e grava em `rpt.tbl_machine_alarms`
