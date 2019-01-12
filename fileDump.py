# Sample Python script for dumping the contents of a database

from dg.RecordDAO import RecordDAO

dao = RecordDAO()
recs = dao.getAll()

print(str(len(recs)) + ' record(s) retrieved')

for rec in recs:
  print(str(rec.guid) + ' last modified on ' + str(rec.modificationDate) + ' status is ' + rec.status)