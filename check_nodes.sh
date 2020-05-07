namespace=$1
list=$2
ar=('serverless' 'swarm' 'openfaas-test'  'intel-cat' 'galaxy-gpu')
for name in "${ar[@]}"
do
echo $name
echo "worker"
kubectl get pods -o wide --field-selector spec.nodeName=$name| grep worker | wc -l
echo "asr"
kubectl get pods -o wide --field-selector spec.nodeName=$name| grep asr | wc -l
echo "nlp"
kubectl get pods -o wide --field-selector spec.nodeName=$name| grep nlp | wc -l
echo "qa"
kubectl get pods -o wide --field-selector spec.nodeName=$name| grep qa | wc -l
if [ "$list" == 1 ]
then
kubectl get pods -o wide --field-selector spec.nodeName=$name
fi
done
