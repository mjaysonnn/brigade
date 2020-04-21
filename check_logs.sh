pod="$1"
namespace="$2"
for entry in $(kubectl get pods -n $namespace | grep $pod | cut -d" " -f 1); do echo $entry ;kubectl describe pod $entry -n $namespace| grep -i "Start time";time=$(echo $(kubectl describe pod $entry -n $namespace| grep -i "Finished" |cut -d, -f 2 | cut -d+ -f 1)) ;echo " time is  $time" ;  echo $(date -d $time + "%s"); done
