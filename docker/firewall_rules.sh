sudo systemctl start ufw
sudo systemctl enable ufw
sudo ufw deny in 9092 & sudo ufw deny in 9092/tcp & sudo ufw deny in 9092/udp
sudo ufw deny in 9093 & sudo ufw deny in 9093/tcp & sudo ufw deny in 9093/udp
sudo ufw deny in 5432 & sudo ufw deny in 5432/tcp & sudo ufw deny in 5432/udp
sudo ufw disable
sudo ufw enable
sudo ufw reload
service iptables restart
