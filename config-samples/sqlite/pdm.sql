-- database: c:\Git\pyBPPIBridge\bppiconfig.sqlite3

-- Use the ▷ button in the top right corner to run the entire file.

DROP TABLE CFG_TABLE;
CREATE TABLE  CFG_BPPI (
    ID INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL,
    DESCRIPTION TEXT
)