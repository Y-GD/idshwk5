from sklearn.ensemble import RandomForestClassifier
import re

domainlist = []


class Domain:
    def __init__(self, _name, _label, _namelength, _number):
        self.name = _name
        self.label = _label
        self.length = _namelength
        self.number = _number

    def returnName(self):
        return self.name

    def returnData(self):
        return [self.length, self.number]

    def returnLabel(self):
        if self.label == "dga":
            return 1
        else:
            return 0


def initData(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            tokens = line.split(",")
            name = tokens[0]
            label = tokens[1]
            namelength = len(name)
            pattern = re.compile(r'\d')
            list = re.findall(pattern, name)
            number = len(list)
            domainlist.append(Domain(name, label, namelength, number))


def main():
    initData("train.txt")
    featureMatrix = []
    labelList = []
    for item in domainlist:
        featureMatrix.append(item.returnData())
        labelList.append(item.returnLabel())

    clf = RandomForestClassifier(random_state=0)
    clf.fit(featureMatrix, labelList)
    with open("test.txt") as f:
        with open("result.txt", 'w') as m:
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                namelength = len(line)
                pattern = re.compile(r'\d')
                number = len(re.findall(pattern, line))
                if (int(clf.predict([[namelength, number]])) == 1):
                    content = line + "," + "dga\n"
                    m.write(content)
                else:
                    content = line + "," + "notdga\n"
                    m.write(content)


if __name__ == '__main__':
    main()
    print("done")
