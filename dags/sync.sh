export REM_HOST="storage.lightmeter.io"
#scp -r -P2223 * admin@$REM_HOST:/home/admin/data-pipeline/ 
rsync -urltv -e 'ssh -p2223 -l admin' --delete --copy-links . $REM_HOST:/home/admin/data-pipeline/
