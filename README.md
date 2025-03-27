Data:

SELECT recordid,campaigninvitationid, talkpushcandidateid,campaigntitle,firstname,lastname, invitationdt,source,assignedmanager,repeatapplication,completionmethod,folder,worklocation,campaign_type,campaign_site,delayinvitationcompletionseconds
FROM talkpush.dbo.tbltalkpushcandidateinfo 
WHERE INVITATIONDT >= '03/01/2024' AND INVITATIONDT < '03/01/2025' 
AND CRMINSTANCE LIKE '%dava%';
