import yara
text = "this contains keylogger backdoor"
rule = """
rule keywords
{
    strings:
    $a = "keylogger"
    $b = "backdoor"
    $c = "trojan"
    
    condition: 
    any of them

}


"""
print(yara.compile(source=rule).match(data=text))
