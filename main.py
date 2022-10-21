class Rotor:
    def __init__(self, number, alphabet, baseRotation, ringSetting, rotorPositioninEnigma):
        self.number = number
        self.controlAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.alphabet = alphabet
        self.rotation = baseRotation
        self.ringSetting = int(ringSetting) - 1
        self.rotorPosition = rotorPositioninEnigma

    def rotate(self):
        self.rotation = self.rotation + 1

    def interpret(self, pressedChar):
        interpretedCharIndex = (self.controlAlphabet.find(pressedChar) + self.rotation - self.ringSetting) % 26
        skewedChar = self.alphabet[int(interpretedCharIndex)]
        deskewedCharIndex = (self.controlAlphabet.find(skewedChar) - self.rotation + self.ringSetting) % 26
        return self.controlAlphabet[int(deskewedCharIndex)]

    def backwardsInterpret(self, pressedChar):
        interpretedCharIndex = (self.controlAlphabet.find(pressedChar) + self.rotation - self.ringSetting) % 26
        skewedCharControl = self.controlAlphabet[int(interpretedCharIndex)]
        skewedCharIndex = self.alphabet.find(skewedCharControl)
        skewedChar = self.controlAlphabet[int(skewedCharIndex)]
        deskewedCharIndex = (self.controlAlphabet.find(skewedChar) - self.rotation + self.ringSetting) % 26
        return self.controlAlphabet[int(deskewedCharIndex)]

def chooseRotors(rotorString):
    if rotorString[0] != "#":
        raise Exception("Invalid rotorString, expected # as first character!")
    rotorString = rotorString[2:]
    rotorArray = rotorString.split(" ")
    return rotorArray

def converOffsetCharToNumber(offsetChar):
    return ord(offsetChar.upper()) - ord("A")

def initPlugboard(plugboardString):
    switcheroos = plugboardString.split(" ")
    return switcheroos

def checkPlugboard(plugboard, checkedChar):
    if plugboard == ['']:
        return checkedChar
    for switcheroo in plugboard:
        if (checkedChar == switcheroo[0]):
            return switcheroo[1]
    for switcheroo in plugboard:
        if (checkedChar == switcheroo[1]):
            return switcheroo[0]
    return checkedChar

def main():
    notchPositions = {
        "I" : "Q",
        "II" : "E",
        "III" : "V",
        "IV" : "J",
        "V" : "Z"
    }
    with open('rotors.txt') as f:
        rotorLines = f.readlines()
    with open('reflectors.txt') as f:
        reflectorLines = f.readlines()
    with open("plugboard.txt") as data:
        dataLines = data.readlines()
        rotorAndPlugboard = dataLines[0].split("-")
        rotors = chooseRotors(rotorAndPlugboard[0][:-1])

        realRotors = []
        for rotorData in rotors:
            settings = rotorData.split(':')
            rotorSetting = settings[0]
            offsetSetting = converOffsetCharToNumber(settings[1])
            ringSetting = settings[2]
            searchLength = len(rotorSetting)
            for rotorLine in rotorLines:
                if (rotorLine[:searchLength] == rotorSetting):
                    rotor = Rotor(rotorSetting, rotorLine[searchLength + 2:-1], offsetSetting, ringSetting , len(realRotors) + 1)
                    realRotors.append(rotor)
                    break

        plugboard = initPlugboard(rotorAndPlugboard[1][1:])

        plainText = dataLines[1][:-1]
        cipherText = []
        controlAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for plainChar in plainText:
            print(controlAlphabet[realRotors[0].rotation % 26] +''+ controlAlphabet[realRotors[1].rotation % 26] +''+ controlAlphabet[realRotors[2].rotation % 26])
            if notchPositions[realRotors[2].number] == controlAlphabet[realRotors[2].rotation % 26] and notchPositions[realRotors[1].number] == controlAlphabet[realRotors[1].rotation % 26]:
                realRotors[2].rotate()
                realRotors[1].rotate()
                realRotors[0].rotate()
            elif notchPositions[realRotors[2].number] == controlAlphabet[realRotors[2].rotation % 26]:
                realRotors[2].rotate()
                realRotors[1].rotate()
            else:
                realRotors[2].rotate()
            print("Plain:" + plainChar)
            newChar = checkPlugboard(plugboard, plainChar)
            print("Plugboard:" + newChar)
            newChar = realRotors[2].interpret(newChar)
            print("Rotor III: " + newChar)
            newChar = realRotors[1].interpret(newChar)
            print("Rotor II: " + newChar)
            newChar = realRotors[0].interpret(newChar)
            print("Rotor I: " + newChar)

            reflector = Rotor("R", reflectorLines[1][3:], 0, 1, 1)
            newChar = reflector.interpret(newChar)
            print("Reflector: " + newChar)

            newChar = realRotors[0].backwardsInterpret(newChar)
            print("Rotor I: " + newChar)
            newChar = realRotors[1].backwardsInterpret(newChar)
            print("Rotor II: " + newChar)
            newChar = realRotors[2].backwardsInterpret(newChar)
            print("Rotor III: " + newChar)
            newChar = checkPlugboard(plugboard, newChar)
            print("Plugboard:" + newChar)
            print("---------------------------")
            cipherText.append(newChar)
        print(cipherText)

if __name__ == "__main__":
    main()