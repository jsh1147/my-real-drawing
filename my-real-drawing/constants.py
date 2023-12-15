class Pointer:
    @property
    def SIZE(self): return 96


class Project:
    @property
    def NAME(self): return 'My Real Drawing'


class State:
    @property
    def MOVE(self): return 'move'
    @property
    def DRAW(self): return 'draw'
    @property
    def CLICK(self): return 'click'
