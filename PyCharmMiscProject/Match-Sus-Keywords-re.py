import re
text = "This contains a keylogger backdoor"
pattern = r"(keylogger|backdoor|trojan)"
print(re.findall(pattern, text))