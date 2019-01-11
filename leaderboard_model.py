import csv

class LeaderboardModel:
    def __init__(self):
        self.B = self.CSVreader('./sav/beginner_leaderboard.csv')
        self.I = self.CSVreader('./sav/intermediate_leaderboard.csv')
        self.E = self.CSVreader('./sav/expert_leaderboard.csv')


    def CSVreader(self,path):
        with open(path) as f:
            reader = csv.reader(f,delimiter=',', quoting=csv.QUOTE_NONE)
            rows = []
            for row in reader:
                rows.append(row)
        return rows


    def CSVwrite(self,csvData,path):
        with open(path, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()


    def getFile(self):
        return self.B,self.I,self.E

    def order(self,A):
        A.sort(key=lambda x: int(x[1]))
