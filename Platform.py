from Block import Block
class Platform(Block):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.color='blue'