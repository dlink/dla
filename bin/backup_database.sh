today=`date +"%Y-%m-%d"`
dump_filepath=/data/backups/db/dla/dla_${today}.dump.gz
mysqldump --login-path=dla dla | gzip > $dump_filepath
echo $dump_filepath created
