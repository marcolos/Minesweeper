import csv

# Chiamo la save quando esco
class Save:
    def __init__(self,controller=None):
        status = controller.model.getStatus()
        counter = controller.model.getCounter()
        n_caselline_open = controller.model.get_n_caselline_open()
        size = controller.model.getSize()
        n_mines = controller.model.get_n_mines()
        n_caselline_flagged = controller.model.get_n_caselline_flagged()

        caselline = controller.model.getCaselline()
        tmp=[]
        matrice=[]
        for x in range(0, size):
            for y in range(0, size):
                c = str(caselline[x][y].is_mine)+" "+str(caselline[x][y].adjacent_n)+" "+str(caselline[x][y].is_revealed)+" "+str(caselline[x][y].is_flagged)
                tmp.append(c)
            matrice.append(tmp)
            tmp=[]

            if x == size-1:
                tmp2 = [ str(status), str(counter), str(n_caselline_open), str(size), str(n_mines), str(n_caselline_flagged) ]
                matrice.append(tmp2)

            self.CSVwrite(matrice)


    def CSVwrite(self,csvData):
        with open('./sav/save.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)

        csvFile.close()


class Resume:
    def __init__(self):
        self.A = self.CSVreader('./sav/save.csv')

        len = self.A.__len__()
        self.status = int(self.A[len-1][0])
        self.counter = int(self.A[len - 1][1])
        self.n_caselline_open = int(self.A[len - 1][2])
        self.size = int(self.A[len - 1][3])
        self.n_mines = int(self.A[len - 1][4])
        self.n_caselline_flagged = int(self.A[len - 1][5])

        self.A.pop()

    def CSVreader(self,path):
        with open(path) as f:
            reader = csv.reader(f,delimiter=',', quoting=csv.QUOTE_NONE)
            rows = []
            for row in reader:
                rows.append(row)
        return rows

    def getMatrix(self):
        return self.A

    def getValue(self):
        return self.status,self.counter,self.n_caselline_open,self.size,self.n_mines,self.n_caselline_flagged

