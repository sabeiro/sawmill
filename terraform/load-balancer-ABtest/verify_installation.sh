 for i in `seq 1 5`; do curl $(terraform output -raw lb_dns_name); done
