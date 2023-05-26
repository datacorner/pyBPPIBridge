SELECT logid,sessionnumber,stagename,pagename,result,startdatetime, stagetype, 
        IIF(processname IS NULL, 'BP OBJECT', 'BP PROCESS') as OBJECT_TYPE , 
        IIF(processname IS NULL, objectname, processname) as OBJECT_NAME 
FROM BPASessionLog_NonUnicode 
WHERE sessionnumber IN (SELECT distinct sessionnumber  FROM BPASessionLog_NonUnicode WHERE processname = 'Bulk IFA Application Process')