import re
import yara

text = "Year 2002, 1993, 20, 10, 4"

## Python regex

pattern = r"\b\d{4}\b"
print("Regex:", re.findall(pattern, text))

## Yara rules
rule = """
rule year
    {
    strings:
    $y = /\\b\\d{4}\\b/

    condition:
    $y
    }

"""
print("YARA:", yara.compile(source=rule).match(data=text))
