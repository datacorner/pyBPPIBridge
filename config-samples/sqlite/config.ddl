CREATE TABLE CFG_BPPISERVER ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT NOT NULL    ,
	DESCRIPTION          TEXT     ,
	TOKEN                TEXT     ,
	URL                  TEXT     
 );

CREATE TABLE CFG_BPPI_REPO_TABLE ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT NOT NULL    ,
	DESCRIPTION          TEXT     
 );

CREATE TABLE CFG_BPPI_REPO_TODO ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT NOT NULL    ,
	DESCRIPTION          TEXT     
 );

CREATE TABLE CFG_BP_API ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	SSL_VERIFICATION     BIT  DEFAULT 0   ,
	CLIENT_ID            TEXT     ,
	CLIENT_SECRET        TEXT     ,
	AUTHENTICATION_URL   TEXT     ,
	API_URL              TEXT     ,
	PAGE_SIZE            INTEGER     
 );

CREATE TABLE CFG_BP_PARAMS ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT(100)     
 );

CREATE TABLE CFG_BP_STAGES ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	CODE                 TEXT     ,
	NAME                 TEXT(100)     
 );

CREATE TABLE CFG_EVENTMAP_TABLETYPE ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	TABLE_TYPE           TEXT     
 );

CREATE TABLE CFG_FILE ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	"TYPE"               TEXT     ,
	SEPARATOR            TEXT     ,
	DESCRIPTION          TEXT     
 );

CREATE TABLE CFG_ODBC_CONNECTION ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	CONNECTION_STRING    TEXT     ,
	QUERY                TEXT     
 );

CREATE TABLE CFG_OTHER ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	LOG_FOLDER           TEXT     ,
	LOG_FILENAME         TEXT     ,
	LOG_LEVEL            TEXT     ,
	LOG_FORMAT           TEXT     
 );

CREATE TABLE CFG_SAP ( 
	ASHOST               TEXT     ,
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	CLIENT               TEXT     ,
	SYSNR                TEXT     ,
	USER                 TEXT     ,
	PASSWORD             TEXT     ,
	ROUTER               TEXT     ,
	RFCTABLE             TEXT     ,
	RFCFIELDS            TEXT     ,
	ROWLIMIT             INTEGER     
 );

CREATE TABLE CFG_SOURCETYPE ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT     
 );

CREATE TABLE CFG_BP_REPO ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	PROCESS_NAME         TEXT     ,
	INCLUDE_VBO          BIT  DEFAULT 1   ,
	UNICODE_SUPPORT      BIT  DEFAULT 0   ,
	START_END_FILTER     BIT  DEFAULT 1   ,
	DELTA_LOAD           BIT  DEFAULT 1   ,
	DELTA_TAG_FILE       TEXT     ,
	FK_ODBC_ID           INTEGER NOT NULL    ,
	FOREIGN KEY ( FK_ODBC_ID ) REFERENCES CFG_ODBC_CONNECTION( ID )  
 );

CREATE TABLE CFG_BP_STAGE_FILTERS ( 
	FK_BPSTAGE_ID        INTEGER NOT NULL    ,
	FK_BPREPO_ID         INTEGER NOT NULL    ,
	CONSTRAINT pk_CFG_BPPI_BPSTAGES_FILTER PRIMARY KEY ( FK_BPSTAGE_ID, FK_BPREPO_ID ),
	FOREIGN KEY ( FK_BPSTAGE_ID ) REFERENCES CFG_BP_STAGES( ID )  ,
	FOREIGN KEY ( FK_BPREPO_ID ) REFERENCES CFG_BP_REPO( ID )  
 );

CREATE TABLE CFG_EVENTMAP ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	MAP_TABLE            TEXT     ,
	MAP_COLUMN           TEXT     ,
	EVENTMAP_TYPE_ID     INTEGER NOT NULL    ,
	FOREIGN KEY ( EVENTMAP_TYPE_ID ) REFERENCES CFG_EVENTMAP_TABLETYPE( ID )  
 );

CREATE TABLE CFG_PIPELINE ( 
	ID                   INTEGER NOT NULL  PRIMARY KEY  ,
	NAME                 TEXT NOT NULL    ,
	DESCRIPTION          TEXT     ,
	FK_SERVER_ID         INTEGER NOT NULL    ,
	FK_REPO_TABLE_ID     INTEGER NOT NULL    ,
	FK_REPO_TODO_ID      INTEGER     ,
	FK_OTHER_ID          INTEGER NOT NULL    ,
	FK_EVENTMAP_ID       INTEGER     ,
	FK_BPREPO_ID         INTEGER     ,
	FK_BPAPI_ID          INTEGER     ,
	FK_FILE_ID           INTEGER     ,
	FK_SAP_ID            INTEGER     ,
	SOURCE_TYPE_ID       INTEGER NOT NULL    ,
	FOREIGN KEY ( FK_OTHER_ID ) REFERENCES CFG_OTHER( ID )  ,
	FOREIGN KEY ( FK_SERVER_ID ) REFERENCES CFG_BPPISERVER( ID )  ,
	FOREIGN KEY ( FK_REPO_TABLE_ID ) REFERENCES CFG_BPPI_REPO_TABLE( ID )  ,
	FOREIGN KEY ( FK_REPO_TODO_ID ) REFERENCES CFG_BPPI_REPO_TODO( ID )  ,
	FOREIGN KEY ( FK_EVENTMAP_ID ) REFERENCES CFG_EVENTMAP( ID )  ,
	FOREIGN KEY ( FK_BPREPO_ID ) REFERENCES CFG_BP_REPO( ID )  ,
	FOREIGN KEY ( FK_BPAPI_ID ) REFERENCES CFG_BP_API( ID )  ,
	FOREIGN KEY ( FK_FILE_ID ) REFERENCES CFG_FILE( ID )  ,
	FOREIGN KEY ( FK_SAP_ID ) REFERENCES CFG_SAP( ID )  ,
	FOREIGN KEY ( SOURCE_TYPE_ID ) REFERENCES CFG_SOURCETYPE( ID )  
 );

CREATE TABLE CFG_BP_PARAMS_COLLECT ( 
	FK_PARAMS_ID         INTEGER NOT NULL    ,
	FK_BPREPO_ID         INTEGER NOT NULL    ,
	CONSTRAINT pk_CFG_BPPI_BPPARAMS_LIST PRIMARY KEY ( FK_PARAMS_ID, FK_BPREPO_ID ),
	FOREIGN KEY ( FK_PARAMS_ID ) REFERENCES CFG_BP_PARAMS( ID )  ,
	FOREIGN KEY ( FK_BPREPO_ID ) REFERENCES CFG_BP_REPO( ID )  
 );

CREATE VIEW VIEW_GET_CONFIG_BLUEPRISM_REPO AS 
SELECT pipeline.ID as ID,
       server.URL AS bppi_url, 
       server.TOKEN AS bppi_token, 
       bppitable.NAME AS bppi_table, 
       other.LOG_FOLDER AS other_logfolder, 
       other.LOG_FILENAME AS other_logfilename, 
       other.LOG_LEVEL AS other_loglevel, 
       other.LOG_FORMAT AS other_logformat, 
       bppitodo.NAME AS bppi_todolist, 
       src.NAME AS sourcetype, 
	   cbr.PROCESS_NAME AS blueprism_processname, 
	   cbr.INCLUDE_VBO AS blueprism_includevbo, 
	   cbr.UNICODE_SUPPORT AS blueprism_unicode, 
	   cbr.START_END_FILTER AS blueprism_startendfilter, 
	   cbr.DELTA_LOAD AS blueprism_delta, 
	   cbr.DELTA_TAG_FILE AS blueprism_deltafile, 
	   coc.CONNECTION_STRING AS database_connectionstring, 
	   coc.QUERY AS database_query
FROM CFG_PIPELINE pipeline 
	LEFT JOIN CFG_BPPISERVER server ON ( server.ID = pipeline.FK_SERVER_ID  )  
	LEFT JOIN CFG_BPPI_REPO_TABLE bppitable ON ( bppitable.ID = pipeline.FK_REPO_TABLE_ID  )  
	LEFT JOIN CFG_OTHER other ON ( other.ID = pipeline.FK_OTHER_ID  )  
	LEFT JOIN CFG_BPPI_REPO_TODO bppitodo ON ( bppitodo.ID = pipeline.FK_REPO_TODO_ID  )  
	LEFT JOIN CFG_SOURCETYPE src ON ( src.ID = pipeline.SOURCE_TYPE_ID  )  
	LEFT JOIN CFG_BP_REPO cbr ON ( cbr.ID = pipeline.FK_BPREPO_ID  )  
	LEFT JOIN CFG_ODBC_CONNECTION coc ON ( coc.ID = cbr.FK_ODBC_ID  ) 
WHERE src.NAME = "bprepo";

CREATE VIEW VIEW_GET_FULLCONFIG_BLUEPRISM_REPO AS 
SELECT cfg.*, 
        "sqlite3" AS configsource,
        stg.STAGEFILTERLIST AS blueprism_stagetypefilters,  
        prm.PARAMLIST AS blueprism_parameters 
FROM VIEW_GET_CONFIG_BLUEPRISM_REPO cfg
LEFT JOIN VIEW_GET_STAGEFILTERSLIST stg ON cfg.ID = stg.CONFIG_ID
LEFT JOIN VIEW_GET_PARAMLIST prm ON  cfg.ID = stg.CONFIG_ID;

CREATE VIEW VIEW_GET_PARAMLIST AS 
SELECT cbp.ID AS CONFIG_ID,
       group_concat(cbp.NAME) AS PARAMLIST
FROM CFG_BP_PARAMS_COLLECT params 
	INNER JOIN CFG_BP_PARAMS cbp ON ( cbp.ID = params.FK_PARAMS_ID  );

CREATE VIEW VIEW_GET_STAGEFILTERSLIST AS  
SELECT stg.ID AS CONFIG_ID,
       group_concat(stg.CODE) AS STAGEFILTERLIST
FROM CFG_BP_STAGE_FILTERS stages 
	INNER JOIN CFG_BP_STAGES stg ON ( stg.ID = stages.FK_BPSTAGE_ID  );

