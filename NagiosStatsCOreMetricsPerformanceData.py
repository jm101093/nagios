#!/opt/omd/versions/1.6.0p20.cre/bin/ python2.7
# NagiosStats check_mk local check for graphing latency of running checks in the nagios core
#by Jeremy McLaurin
import re
import commands

text = commands.getoutput('sudo /opt/omd/versions/1.6.0p20.cre/bin/nagiostats /opt/omd/sites/node/etc/nagios/nagios.cfg')

# Define regex patterns to extract the required information
active_service_latency_pattern = r"Active Service Latency:\s+(\d+\.\d+) \/ (\d+\.\d+) \/ (\d+\.\d+) sec"
active_service_execution_time_pattern = r"Active Service Execution Time:\s+(\d+\.\d+) \/ (\d+\.\d+) \/ (\d+\.\d+) sec"
active_host_latency_pattern = r"Active Host Latency:\s+(\d+\.\d+) \/ (\d+\.\d+) \/ (\d+\.\d+) sec"
active_host_execution_time_pattern = r"Active Host Execution Time:\s+(\d+\.\d+) \/ (\d+\.\d+) \/ (\d+\.\d+) sec"

# Extract the information using the regex patterns
active_service_latency_match = re.search(active_service_latency_pattern, text)
active_service_execution_time_match = re.search(active_service_execution_time_pattern, text)
active_host_latency_match = re.search(active_host_latency_pattern, text)
active_host_execution_time_match = re.search(active_host_execution_time_pattern, text)

# Print the extracted information in the desired format
print("P CheckMK_Core_Active_Service_Latency minLatency={}|MaxLatency={}|AverageLatency={}".format(active_service_latency_match.group(1), active_service_latency_match.group(2), active_service_latency_match.group(3)))
print("P CheckMK_Core_Active_Service_Execution_Time minExecutionTime={}|MaxExecutionTime={}|AverageExecutionTime={}".format(active_service_execution_time_match.group(1), active_service_execution_time_match.group(2), active_service_execution_time_match.group(3)))
print("P CheckMK_Core_Active_Host_Latency minLatency={}|MaxLatency={}|AverageLatency={}".format(active_host_latency_match.group(1), active_host_latency_match.group(2), active_host_latency_match.group(3)))
print("P CheckMK_Core_Active_Host_Execution_Time minExecutionTime={}|MaxExecutionTime={}|AverageExecutionTime={}".format(active_host_execution_time_match.group(1), active_host_execution_time_match.group(2), active_host_execution_time_match.group(3)))
