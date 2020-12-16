/*Script to query faulty GPS Units within a date range */

/*User Defined Variables: in 'YYYY-MM-DD'
*/

SET @SearchFromThisDate = '2019-12-20';

SET @SSIRange_Min = 70000;
SET @SSIRange_Max = 90000;

/*CODE*/
DROP TABLE IF EXISTS g;
CREATE TEMPORARY TABLE g (INDEX(CallingSsi)) AS
  (SELECT DISTINCT s1.CallingSsi FROM sdsdata s1
    WHERE s1.UserDataLength = 129 and s1.Timestamp >= @SearchFromThisDate
    AND s1.CallingSsi >= @SSIRange_Min and s1.CallingSsi < @SSIRange_Max );
    
DROP TABLE IF EXISTS gTemp;
CREATE TEMPORARY TABLE gTemp (INDEX(CallingSSi)) AS
(SELECT DISTINCT 
s.CallingSsi
 FROM sdsdata s
  WHERE
        s.UserDataLength = 44 and
        s.Timestamp >= @SearchFromThisDate and
        s.CallingSsi >= @SSIRange_Min and s.CallingSsi < @SSIRange_Max and
		NOT EXISTS (SELECT * FROM g WHERE g.CallingSsi = s.CallingSsi)
ORDER BY s.CallingSsi);

SELECT 
	Subr.SSI,
    Subr.Description,
    Subr.MarkedForDeletion,
    Subr.Timestamp
	FROM subscriber Subr
      WHERE EXISTS(SELECT * FROM gTemp WHERE gTEMP.CallingSSi = Subr.SSI)
ORDER BY Subr.SSI
		

