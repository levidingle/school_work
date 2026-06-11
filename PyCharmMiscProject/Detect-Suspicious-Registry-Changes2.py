import yara
text = "This contains HKEY_CURRENT_USER"
rule="""
rule Registry_Persistence
{
    strings:
    $a = "HKEY_CURRENT_USER"
    $b = "RunOnce"
    $c = "Run"
    
    condition:
    any of them
}
"""

print(yara.compile(source=rule).match(data=text))