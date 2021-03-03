

class PropertiesManager:

    propertiesDictionary = {}

    def __init__(self):
        propertiesFile = open("/com/company/resources/settings/application.properties", "a")

        while (True):
            line = propertiesFile.readline()
            if not line:
                break

            propNameVal = line.split(" = ")
            if (len(propNameVal) != 2):
                print("ERROR: Issue with property. Text value: " + line)
            else:
                self.propertiesDictionary[propNameVal[0]] = propNameVal[1]



    def getProperty(self, propertyName):
        returnVal = self.propertiesDictionary.get(propertyName)
        if not returnVal:
            print("ERROR: No propert with name matching: " + propertyName + " could be found.")
        else:
            return returnVal