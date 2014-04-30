commandFile = open("./valid.brocc")
commands = []

for text in commandFile.readlines():
    commands.append(text.rstrip())
    
def ValidCommand(text):
    text = text.rstrip('\r\n')
    if text in commands:
        print('----------------- VALID COMMAND : ' + text + ' -----------------')
        return True
    print('----------------- INVALID COMMAND : ' + text + ' -----------------')
    return False
