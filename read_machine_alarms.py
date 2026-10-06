import os
from pathlib import Path

import requests
import pyodbc
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

URL = "http://137.131.185.161:8102/machine-alarms"
SERVER = os.environ["CW_SERVER"]
DATABASE = os.environ["CW_DATABASE"]
USER = os.environ["CW_USER"]
PASSWORD = os.environ["CW_PASSWORD"]

SCHEMA = "rpt"
TABLE = "tbl_machine_alarms"
FULL_NAME = f"[{SCHEMA}].[{TABLE}]"

response = requests.get(URL, headers={"Authorization": "Bearer x"}, timeout=10)
response.raise_for_status()
alarms = response.json()["data"]

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}"
)
cur = conn.cursor()

cur.execute(f"IF SCHEMA_ID('{SCHEMA}') IS NULL EXEC('CREATE SCHEMA {SCHEMA}')")

cur.execute(f"""
IF OBJECT_ID('{SCHEMA}.{TABLE}', 'U') IS NULL
CREATE TABLE {FULL_NAME} (
    [AlarmId] NVARCHAR(50) NOT NULL,
    [OperatorId] NVARCHAR(50) NULL,
    [OperatorName] NVARCHAR(200) NULL,
    [LineId] NVARCHAR(50) NULL,
    [AlarmType] NVARCHAR(100) NULL,
    [AlarmTime] DATETIME2 NULL,
    [AlarmDate] DATE NULL,
    [Severity] NVARCHAR(20) NULL,
    [WorkCenter] NVARCHAR(100) NULL,
    [Plant] NVARCHAR(100) NULL,
    [MaxTemp] FLOAT NULL,
    [MaxDeviation] FLOAT NULL,
    [EventLogUrl] NVARCHAR(500) NULL,
    [LoadDateTime] DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT [PK_{TABLE}] PRIMARY KEY CLUSTERED ([AlarmId])
)
""")
conn.commit()

for a in alarms:
    location = a.get("location") or {}
    cur.execute(f"DELETE FROM {FULL_NAME} WHERE [AlarmId] = ?", a["id"])
    cur.execute(
        f"""
        INSERT INTO {FULL_NAME}
            ([AlarmId],[OperatorId],[OperatorName],[LineId],[AlarmType],[AlarmTime],[AlarmDate],
             [Severity],[WorkCenter],[Plant],[MaxTemp],[MaxDeviation],[EventLogUrl])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        a["id"], a.get("operatorId"), a.get("operatorName"), a.get("lineId"), a.get("alarmType"),
        a.get("time"), a.get("date"), a.get("severity"),
        location.get("workCenter"), location.get("plant"),
        a.get("maxTemp"), a.get("maxDeviation"), a.get("eventLogUrl"),
    )

conn.commit()
print(f"Loaded {len(alarms)} alarms into {SCHEMA}.{TABLE}")
