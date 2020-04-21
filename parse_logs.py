import subprocess
import json
output = subprocess.check_output("kubectl get pod imc-01e6czwbz42wvs9h0myknfczgj -o json", shell=True)
y = json.loads(output)
print y

