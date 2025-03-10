class Duck:
    def swim(self):
        print ("Duck can Swim")
    def fly(self):
        print ("Dock Can Fly")

class Whale:
    def swim(self):
        print ("Whale can Swim")

for animal in [Duck(), Whale()]:
    animal.swim()
    animal.fly()
