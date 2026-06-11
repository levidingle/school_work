import yara
text = "Hash A1B2C3D4"
rule = """
rule Match_Hex
{
    strings:
    $h = /\b[A-Fa-f0-9]{8}\b/

    
    condition:
    $h


}
"""
print(yara.compile(source=rule).match(data=text))