podname=$1
namespace=$2
ar=('frontend' 'asr-slackware10' 'nlp-slackware10'  'qa-slackware10' 'vacuum' 'worker')
echo $podname,$ar
for name in "${ar[@]}"
do
echo $name
kubectl -n brigade get pods -n $namespace | cut -d" " -f1 | awk "/$name/{print}" | xargs  kubectl -n $namespace delete pod
done
