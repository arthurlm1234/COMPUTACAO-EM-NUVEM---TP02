kubectl delete deploy playlist-recommender-deployment

cd kubernetes
kubectl -n arthurmadureira apply -f pvc.yaml
kubectl -n arthurmadureira apply -f deployment.yaml
kubectl -n arthurmadureira apply -f service.yaml
cd ..