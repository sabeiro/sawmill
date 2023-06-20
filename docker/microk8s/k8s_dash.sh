microk8s enable dns dashboard storage
sudo ufw allow in on cni0 && sudo ufw allow out on cni0
sudo ufw default allow routed
microk8s kubectl get all --all-namespaces
microk8s kubectl create token default
#token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
#microk8s kubectl -n kube-system describe secret $token
#microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
microk8s dashboard-proxy


