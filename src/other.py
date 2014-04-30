import sys
from operator import itemgetter

class ChampData:
    def __init__(self, text):
        self.champDict = {}
        self.sortedChamps = []

        for champ in text.readlines():
            print(champ)
            self.champDict[champ.rstrip()] = 0

    def IsChamp(self, champ):
        print("Checking champ")
        champ = champ.rstrip()
        print(repr(champ))
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

    def SortByVotes(self):
        self.sortedChamps = sorted(self.champDict.items(), key=itemgetter(1), reverse=True)

    def GetWinner(self):
        self.SortByVotes()
        return self.sortedChamps[0]

    def GetTop(self, num):
        self.SortByVotes()
        return self.sortedChamps[0:num]

    def Test(self):
        for champ in self.champDict:
            print (repr(champ))
