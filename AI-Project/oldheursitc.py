 value = 0
        if board.board.count(self.piece) > board.board.count(self.opponentPiece):
            value += 1
        else:
            value -= 1
        for x in range(0,len(board.board)):
            for y in range(0,len(board.board)):
                if board.board[y][x] == self.piece:
                    #control the very centre of board for longivity
                    if x < 2 or x > 5:
                        value -= 1
                    else:
                        value += 1
                    if y < 2 or y > 5:
                        value -= 1
                    else:
                        value += 1

                    movable = True
                    for dx, dy in [(1, 0), (0, 1), (0, -1), (-1, 0)]:

                        #not helpful if the same pieces are right next to each other
                        try:
                            if board.board[y + dy][x + dx] == self.piece:
                                value -= 1
                        except IndexError:
                            pass
                        #Its good to have control of cells in corners for easy kills
                        try:
                            if board.board[y + dy][x + dx] == "X":
                                value += 1
                        except IndexError:
                            pass
                        # Want to move closer to other pieces so you can eliminate them
                        try:
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                value += 1
                        except IndexError:
                            pass
                        #Its good if the piece can move in all directions after moving
                        try:
                            if not board.isValidMove(((x, y), (x + dx, y + dy))):
                                movable = False
                        except IndexError:
                            value -= 1
                        #not good if the new if a move will cant move again
                        try:
                            board.board[y + dy][x + dx]
                        except IndexError:
                            value -= 1
                    if movable:
                        value += 1
                    else:
                        value -= 1
                    #check diagonals
                    for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        try:
                            # you dont want pieces to close togther
                            if board.board[y + dy][x + dx] == self.piece:
                                value -= 1
                        except IndexError:
                            value -= 1
                        try:
                            # you could work to elimate this piece
                            if board.board[y + dy][x + dx] == self.opponentPiece:
                                for dx1, dy1 in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                                    if (x+dx,y+dy) == (dx+dx1,dy+dy1):
                                        continue
                                    if board.board[dy+dy1][dx+dx1] == self.piece:
                                        value += 1
                                    elif board.board[dy+dy1][dx+dx1] == self.opponentPiece:
                                        value -= 1
                        except IndexError:
                            value -= 1
                    for dx, dy in [(2, 0), (0, 2), (0, -2), (-2, 0)]:
                        #looking for close
                        try:
                            if board.board[y + dy][x + dx] == self.piece:
                                value += 1
                        except IndexError:
                            value += 1
        return value