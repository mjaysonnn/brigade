n=$1
namespace=$2
ar=('frontend' 'asr' 'nlp' 'worker' 'qa-' 'vacuum')
for name in "${ar[@]}"
do
echo $name
kubectl -n brigade get pods -n $namespace | cut -d" " -f1 | awk "/$name/{print}" | xargs  kubectl -n $namespace delete pod
done
