import yara
text = "THis contains socket connect"

rule = """
rule Reverse_Shell
{
    strings:
    $a = "cmd.exe"
    $b = "socket"
    $c = "connect"
    
    condition:
    any of them
}


"""
print(yara.compile(source=rule).match(data=text))
