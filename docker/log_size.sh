#sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
sudo du -sch /var/lib/docker/containers/*/*-json.log
echo "" > $(docker inspect --format='{{.LogPath}}' <container_name_or_id>)
