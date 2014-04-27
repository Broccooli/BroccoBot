import sys

class ChampData:
    def __init__(self, text):
        self.champDict = {}        

        for champ in text.readlines():
            print(champ)
            self.champDict[champ.rstrip()] = 0

    def IsChamp(self, champ):
        print("Checking champ")
        champ = champ.rstrip()
        print(champ)
        if champ in self.champDict:
            return True
        else:
            return False

    def GetVotes(self):
        retValue = []
        for champ in self.champDict:
            if self.champDict[champ] > 0:
                retValue.append(champ + ": " + str(self.champDict[champ]))

        return retValue

    def VoteChamp(self, champ):
        if self.IsChamp(champ):
            self.champDict[champ] += 1

    def Test(self):
        for champ in self.champDict:
            print (repr(champ))
