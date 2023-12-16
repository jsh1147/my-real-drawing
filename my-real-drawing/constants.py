class Button:
    # 색상 버튼
    @property
    def COLOR_VALUE(self):
        return [(0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 0),
                (255, 0, 255), (255, 255, 255), (0, 0, 0)]
    @property
    def COLOR_WIDTH(self): return 48
    @property
    def COLOR_HEIGHT(self): return 48
    @property
    def COLOR_GAP(self): return 8

    # 기타 버튼(지우개, 초기화, 변환, 저장, 종료)
    @property
    def ETC_VALUE(self): return ['ERASE', 'RESET', 'REAL', 'SAVE', 'EXIT']
    @property
    def ETC_WIDTH(self): return 84
    @property
    def ETC_HEIGHT(self): return 48
    @property
    def ETC_GAP(self): return 32

class Pointer:
    @property
    def SIZE(self): return 64


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
