set -x
for entry in $(kubectl get pod -n brigade| grep worker | grep "Completed" | cut -d" " -f1 ) 
do                                                                                                                                                
echo $entry                                                                                                                                                  
schedType=$(kubectl logs $entry -n brigade | grep "Job arrival" | cut -d" " -f 12 | cut -d- -f2 | tail -n 1)                                                 
echo "$entry,$schedType"                                                                                                                          
arrivals=$(kubectl logs $entry -n brigade| grep "Job" | cut -d" " -f 9)                                                                                     
arrivalTimes=$(echo $arrivals | sed 's/\n/ /g')                                                                                                   
starttimes=$(kubectl logs $entry -n brigade| grep "asr" | grep "Pending" | tail -n 1 | cut -d" " -f 5)                                                      
starttimes="${starttimes}$(echo " ")$(kubectl logs $entry | grep "nlp" | grep "Pending" | tail -n 1| cut -d" " -f 5)"                             
starttimes="${starttimes}$(echo " ")$(kubectl logs $entry | grep "qa" | grep "Pending" | tail -n 1| cut -d" " -f 5)"                              
finished=$(kubectl logs $entry -n brigade| grep "Succeeded"| cut -d" " -f 5)                                                                                
finishtimes=$(echo $finished | sed 's/\n/ /g')                                                                                                    
#echo "finished $finishedtimes"                                                                                                                   
if [ "$schedType" = "slackaware" ]                                                                                                                
then                                                                                                                                              
echo "$schedType $arrivalTimes $starttimes $finishtimes" >> slackaware_logs                                                                       
#echo "$arrivalTimes, $starttimes, $finishtimes"                                                                                                  
echo "slackaware job"                                                                                                                             
elif [ "$schedType" = "baseline" ]                                                                                                                
then                                                                                                                                              
echo "$schedType $arrivalTimes $starttimes $finishtimes">> baseline_logs                                                                          
#echo "$arrivalTimes, $starttimes, $finishtimes"                                                                                                  
echo "baseline job"                                                                                                                               
elif [ "$schedType" = "slackprediction" ]                                                                                                         
then                                                                                                                                              
echo "$schedType $arrivalTimes $starttimes $finishtimes">> slackprediction_logs                                                                   
#echo "$arrivalTimes, $starttimes, $finishtimes"                                                                                                  
echo "slackprediction job"                                                                                                                        
fi                                                                                                                                                
echo "***************"                                                                                                                            
done  
