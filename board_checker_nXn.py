class Board:
    @staticmethod
    def left_to_right(board, c):
        '''
        board: 2D-board where the matching should be performed
        c: any character to be matched
        
        Return: (True, row_index) if match found | (False, None) otherwise
        
        Scans the given board from left to right for each row
        '''
        for i in range(len(board)):
            current_row=list()
            for j in range(len(board[i])):
                current_row.append(board[i][j])
            if current_row.count(c)==len(board[i]):
                return True,i
        return False,None
    @staticmethod
    def top_to_bottom(board, c):
        '''
        board: 2D-board where the matching should be performed
        c: any character to be matched
        
        Return: (True, column_index) if match found | (False, None) otherwise
        
        Scans the given board from top to bottom for each column
        '''
        for i in range(len(board)):
            current_column = list()
            for j in range(len(board[i])):
                current_column.append(board[j][i])
            if current_column.count(c)==len(board[i]):
                return True,i
        return False, None
    @staticmethod
    def diagonals(board,c):
        '''
        board: 2D-board where the matching should be performed
        c: any character to be matched
        
        Return: (True, 0 | 1) if match found | (False, None) otherwise
        (True, 0): if match found from top-left to bottom-right
        (True, 1): if match found from bottom-left to top-right
        
        Scans the given board diagonally for both  diagonals
        '''
        diagonal0=list()
        diagonal1=list()
        for i in range(len(board)):
            for j in range(len(board)):
                if i==j:
                    diagonal0.append(board[i][j])
                if (i+j)==len(board)-1:
                    diagonal1.append(board[i][j])
        if diagonal0.count(c)==len(board):
            return True,0
        if diagonal1.count(c)==len(board):
            return True,1
        return False,None
    @staticmethod
    def validate(board):
        for row in board:
            if len(row)!=len(board):
                return False
        return True

def check(board, c):
    if Board.validate(board):
        if Board.diagonals(board,c)[0]:
            return True
        if Board.left_to_right(board,c)[0]:
            return True
        if Board.top_to_bottom(board,c)[0]:
            return True
        else:
            return False
    return "Invalid Board !!!"

if __name__=="__main__":
    # l1=[["O","O","X","X"],
    #     ["O","O","X","O"],
    #     ["O","X","_","O"],
    #     ["X","_","X","O"]]

    # l1=[["O","O","X","X","_"],
    #     ["O","O","X","O","_"],
    #     ["O","O","O","O","_"],
    #     ["O","X","X","O","_"],
    #     ["X","_","X","O","O"]]

    # l2=[["O","O","X"],
    #     ["O","O","X"],
    #     ["O","O","O"]]

    l2=[["_","_","X"],
        ["O","X","O"],
        ["X","O","O"]]

    print(check(l2, "O"))