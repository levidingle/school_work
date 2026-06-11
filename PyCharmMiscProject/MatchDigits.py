import re
import yara

text = "Invoice 12345"
pattern = r"\d+"
print(re.findall(pattern, text))

rule = """
rule Digits 
{
strings:
    $a = "/\\d+/"
    
    condition:
    $a    
}

"""
print(yara.compile(source=rule).match(data=text))
