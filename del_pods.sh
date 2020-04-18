name=$1
namespace=$2
echo $name
kubectl -n brigade get pods -n $namespace | cut -d" " -f1 | awk "/$name/{print}" | xargs  kubectl -n $namespace delete pod
