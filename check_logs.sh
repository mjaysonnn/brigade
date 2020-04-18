pod="$1"
namespace="$2"
for entry in $(kubectl get pods -n $namespace | grep $pod | cut -d" " -f 1); do echo $entry ;kubectl describe pod $entry -n $namespace| grep -i "Start time";kubectl describe pod $entry -n $namespace| grep -i "Finished"; done
