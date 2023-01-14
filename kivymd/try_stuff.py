import time
from kivy.clock import Clock

dic = {
    "a": 5,
    "b": 6,
    "c": 7,
    "d": 8,
}    

#"" if a==8 else print("nice")
def do_this(dt):
    print("Juice")

class Foo(object):
    def start(self):
        Clock.schedule_interval(self.callback, 0.5)

    def callback(self, dt):
        print('In callback')


foo = Foo()
foo.start()