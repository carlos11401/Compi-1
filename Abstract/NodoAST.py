class NodoAST():
    def __init__(self, value):
        self.children = []
        self.value = value

    def setChildren(self, children):
        self.children = children

    def addChild(self, valueChild):
        self.children.append(NodoAST(valueChild))

    def addChildren(self, children):
        for hijo in children:
            self.children.append(hijo)

    def addNodeChild(self, child):
        self.children.append(child)

    def addFirstChild(self, valueChild):
        self.children.insert(0,NodoAST(valueChild))

    def addFirstNodeChild(self, child):
        self.children.insert(0,child)

    def getValue(self):
        return str(self.value)

    def setValue(self, value):
        self.value = value

    def getChildren(self):
        return self.children
