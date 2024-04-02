from copy import deepcopy
from board_checker_nXn import check
import time

def timit(func):
    def inner(*args):
        s = time.time()
        out = func(*args)
        print(f"Time taken({func.__name__}): {time.time()-s}")
        return out
    return inner

def check_board(list1,c):
    top_left_to_right = list1[0][0]==c and list1[0][1]==c and list1[0][2]==c
    top_left_to_bottom = list1[0][0]==c and list1[1][0]==c and list1[2][0]==c
    top_left_to_bottom_right = list1[0][0]==c and list1[1][1]==c and list1[2][2]==c

    mid_left_to_right = list1[1][0]==c and list1[1][1]==c and list1[1][2]==c
    mid_top_to_mid_bottom = list1[0][1]==c and list1[1][1]==c and list1[2][1]==c

    bottom_left_to_right = list1[2][0]==c and list1[2][1]==c and list1[2][2]==c
    bottom_right_to_top = list1[2][2]==c and list1[1][2]==c and list1[0][2]==c
    bottom_left_to_top_right = list1[2][0]==c and list1[1][1]==c and list1[0][2]==c

    if top_left_to_right or top_left_to_bottom or top_left_to_bottom_right or mid_left_to_right or mid_top_to_mid_bottom or bottom_left_to_right or bottom_right_to_top or bottom_left_to_top_right:
        return 1
    return 0

def is_complete(board):
    for row in board:
        for element in row:
            if element=="_":
                return False
    return True

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]!="_":
                return False
    return True

def empty_spaces(board):
    count=0
    for row in board:
        for element in row:
            if element=="_":
                count+=1
    return count

def find_winner(board):
    # if check_board(board, "O"):
    if check(board, "O"):
        return "O"
    # if check_board(board, "X"):
    if check(board, "X"):
        return "X"
    if is_complete(board):
        return "DRAW"
    return "INCOMPLETE GAME"

def calculate_possibilities(board, coords: list, play_as='O',n=0):
    '''Store all the possibile values in the coords list'''
    if n > len(board)+2:
        return
    result = find_winner(board)
    res_len = len(result)
    
    #incomplete section
    if res_len==15:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]=="_":
                    temp_board = deepcopy(board)
                    if n%2==0:
                        if play_as=="X":
                            temp_board[i][j]="X"
                        if play_as=="O":
                            temp_board[i][j]="O"
                    else:
                        if play_as=="X":
                            temp_board[i][j]="O"
                        if play_as=="O":
                            temp_board[i][j]="X"
                    x = calculate_possibilities(temp_board,coords, play_as,n=n+1)
                    coords.append((x, i,j))
        # return calculate_possibilities(temp_board,coords, play_as,n=n+1)
    else:

        #winning section
        if res_len==1:
            return (result,n)
        
        # draw section
        else:
            return ("draw",n)
    
def filter_valid_coords(res):
    if res[0]:
        if len(res[0][0])<=4:
            return True
    return False

def filter_top_coords(res, n):
    if res[0][1]==n:
        return True
    return False

def get_best_coords(board, coords, play_as="O"):
    if is_complete(board):
        return "Game is Completed"
    calculate_possibilities(board,coords, play_as)
    total_coords = list(filter(filter_valid_coords, coords))
    print(len(total_coords))
    total_coords = list(set(total_coords))
    total_coords=sorted(total_coords, key=lambda x: x[0][1], reverse=True)
    
    # print(total_coords)
    # return

    # displaying top 10 choices
    for i in total_coords[-10:]:
        print(i)
    
    if total_coords[-1][0][0]=='draw':
        if len(total_coords)>=2:
            return total_coords[-2][1:]
        else:
            return total_coords[-1][1:]
    else:
        return total_coords[-1][1:]
@timit
def get_best_coords_for_streamlit(board, coords, play_as="O"):
    if is_complete(board):
        return "Game is Completed"
    calculate_possibilities(board,coords, play_as)
    total_coords = list(filter(filter_valid_coords, coords))
    print("\nTotal Calulations:",len(total_coords),"(AI)")
    total_coords = list(set(total_coords))
    total_coords=sorted(total_coords, key=lambda x: x[0][1], reverse=True)
    
    if total_coords[-1][0][0]!="DRAW":
        total_coords = list(filter(lambda x: filter_top_coords(x, total_coords[-1][0][1]), total_coords))
    print("Results evaluated:")
    for i in total_coords:
        print("  ",i)
    return total_coords

if __name__=="__main__":
    # l2 = [["X","O","X"],
    #       ["O","O","X"],
    #       ["X","X","O"]]
    
    # l3 = [["X","O","O"],
    #       ["O","X","X"],
    #       ["O","X","O"]]
    # l4 = [['_', '_', '_'], ['_', '_', '_'], ['X', '_', '_']]

    # l1 = [["_","_","_"],
    #       ["_","_","_"],
    #       ["X","_","_"]]
    
    # l1 = [["O","O","O", "X"],
    #       ["O","O","X", "O"],
    #       ["O","_","_", "X"],
    #       ["X","X","_", "O"]]
    
    l1 = [["_","_","_","_"],
          ["_","X","_","_"],
          ["_","X","O","_"],
          ["O","X","_","_"]]
    # l1 = [['X', '_', 'O'], ['X', 'O', '_'], ['X', 'O', 'X']]
    res_coords=list()
    # print(is_complete(l3))
    # print(calculate_possibilities(l1, res_coords,"O"))
    # print(get_best_coords(l1, res_coords,"O"))
    # print(res_coords)
    # print(get_best_coords_for_streamlit(l1,res_coords,"X"))
    for i in get_best_coords_for_streamlit(l1,res_coords,"X"):
        print(i[1:])
    # print(res_coords)
    # print(empty_spaces(l1))