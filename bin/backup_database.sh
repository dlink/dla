today=`date +"%Y-%m-%d"`
mysqldump --login-path=dla dla | gzip > /data/backups/db/dla_${today}.dump.gz
