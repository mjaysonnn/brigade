podname=$1
namespace=$2
ar=('frontend' 'asr-slack' 'nlp-slack'  'qa-slack' 'vacuum' 'worker')
echo $podname,$ar
for name in "${ar[@]}"
do
echo $name
kubectl get pods -n $namespace | cut -d" " -f1 | awk "/$name/{print}" | xargs  kubectl -n $namespace delete pod
done
