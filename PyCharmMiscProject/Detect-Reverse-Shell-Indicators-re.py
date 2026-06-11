import re
text = "This contains socket connect"

pattern = r"socket|connect|cmd.exe"
print(re.findall(pattern, text))
