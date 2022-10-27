class Test:
    test_list = []

    def __init__(self, element):
        self.element = element
        Test.test_list.append(element)


t1 = Test("Hallo")
t2 = Test("Doei")

#print(Test.test_list)

# Test for duplicates of list
x = [
    ["Timmerman", "Bramer", "Vriezenveen", "Twenterand"],
    ["Timmerman", "Bramer", "Vriezenveen", "Twenterand"]
]

print(x)
print(set(x))