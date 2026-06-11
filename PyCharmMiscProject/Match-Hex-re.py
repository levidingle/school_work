import re
text = "Hash A1B2C3D4"
pattern = r"\b[A-Fa-f0-9]{8}\b"

print(re.findall(pattern, text))
