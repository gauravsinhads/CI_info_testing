Data:

SELECT * FROM talkpush.dbo.tbltalkpushcandidateinfo
WHERE INVITATIONDT >= '01/01/2025' AND INVITATIONDT < '03/01/2025'
AND CRMINSTANCE LIKE '%dava%';
