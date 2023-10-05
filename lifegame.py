class LifeGame:
    def __init__(self):
        self.w = 64
        self.h = 64
        self.board = [0 for _ in range(self.h + 2)]
    
    def set_life(self, x, y):
        offset = (x + 1) // 64 + (y + 1)
        mask = 0x8000000000000000 >> (x & 63)
        self.board[offset] |= mask

    def get_around(self, i):
        c = self.board[i]
        u = self.board[i - 1]
        d = self.board[i + 1]
        l = c >> 1
        r = c << 1
        ul = u >> 1
        ur = u << 1
        dl = d >> 1
        dr = d << 1
        return ul, u, ur, l, c, r, dl, d, dr
    
    def next_gen(self, i):
        ul, u, ur, l, c, r, dl, d, dr = self.get_around(i)
        
        s2 = ul & u
        s1 = ul ^ u
        s0 = ~(ul | u)

        s3 = s2 & ur
        s2 = (s2 & ~ur) | (s1 & ur)
        s1 = (s1 & ~ur) | (s0 & ur)
        s0 &= ~ur

        s3 = (s3 & ~l) | (s2 & l)
        s2 = (s2 & ~l) | (s1 & l)
        s1 = (s1 & ~l) | (s0 & l)
        s0 &= ~l

        s3 = (s3 & ~r) | (s2 & r)
        s2 = (s2 & ~r) | (s1 & r)
        s1 = (s1 & ~r) | (s0 & r)
        s0 &= ~r

        s3 = (s3 & ~dl) | (s2 & dl)
        s2 = (s2 & ~dl) | (s1 & dl)
        s1 = (s1 & ~dl) | (s0 & dl)
        s0 &= ~dl

        s3 = (s3 & ~d) | (s2 & d)
        s2 = (s2 & ~d) | (s1 & d)
        s1 = (s1 & ~d) | (s0 & d)
        s0 &= ~d

        s3 = (s3 & ~dr) | (s2 & dr)
        s2 = (s2 & ~dr) | (s1 & dr)
        s1 = (s1 & ~dr) | (s0 & dr)
        s0 &= ~dr
        
        return (~c & s3) | (c & (s2 | s3))
    
    def next_board(self):
        board = [0]
        for i in range(1, self.h + 1):
            board.append(self.next_gen(i))
        board.append(0)
        self.board = board

    def __str__(self):
        res = ""
        for i in range(1, self.h + 1):
            res += format(self.board[i], f"064b")
            res += "\n"
        return res

if __name__ == "__main__":
    lifegame = LifeGame()
    lifegame.set_life(1, 0)
    lifegame.set_life(1, 1)
    lifegame.set_life(1, 2)
    for _ in range(4):
        print(lifegame)
        print()
        lifegame.next_board()
