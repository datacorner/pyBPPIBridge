SELECT logid, LOG.sessionnumber, stagename, pagename, result,LOG.startdatetime, stagetype, attributexml,
IIF(processname IS NULL, 'BP OBJECT', 'BP PROCESS') as OBJECT_TYPE, 
IIF(processname IS NULL, objectname, processname) as OBJECT_NAME,
BPAResource.name as DWName
FROM $tablelog AS LOG, BPASession, BPAResource
WHERE LOG.sessionnumber IN 
(SELECT distinct sessionnumber  
            FROM $tablelog 
		    WHERE processname = '$processname'
            AND $delta)
AND stagetype NOT IN($stagetypefilters)
AND LOG.sessionnumber = BPASession.sessionnumber
AND BPAResource.resourceid = BPASession.runningresourceid
AND $onlybpprocess