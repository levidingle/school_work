import re
import yara

text = "This file may contain malware."

## Python regex

pattern = r"malware"
if re.search(pattern, text):
    print("We found malware!!!!")

## Yara rules
rule = """
    rule MalwareWord 
    {
    strings:
    $a = "malware"
    
    condition:
    $a
    }

"""
rule = yara.compile(source=rule)
print(rule.match(data=text))



