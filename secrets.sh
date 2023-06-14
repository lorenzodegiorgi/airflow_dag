kubectl create secret generic   airflow-ssh-git-secret   --from-file=id_ed25519=$HOME/.ssh/id_ed25519   --namespace airflow-cluster
