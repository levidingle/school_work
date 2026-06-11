import re
text = "This contains HKEY_CURRENT_USER"
pattern = r"(HKEY_CURRENT_USER|RunOnce|Run)"

print(re.findall(pattern, text))