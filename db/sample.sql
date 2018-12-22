select
*
from
fileproc.file_uploads order by modification_date desc;

select count(id) from fileproc.file_uploads where filehash = '86909456ab1e6ef17cf7aa5af27a3962b7c32df4z' and creation_date >= NOW() - INTERVAL 1 DAY;

select
*
from
fileproc.file_records
where
/*created_date >= '2018-12-04 00:00:00' order by modification_date desc;*/
creation_date >= NOW() - INTERVAL 1 DAY order by modification_date desc;

select record_id from fileproc.file_records where guid = 'bla-1231';

insert into fileproc.file_records (guid,status_cde,request_body,created_date,modification_date) values ('bla-121','SENT','boo123','2018-12-01 22:49:22','2018-12-01 22:49:22');

INSERT INTO `fileproc`.`file_records`
(
`guid`,
`status_cde`,
`request_body`,
`created_date`,
`modification_date`)
VALUES
(
'abcd-11',
'SENT',
'BOO',
now(),
now()
);
