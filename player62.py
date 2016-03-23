import random
import copy

class Player62:
    
    def __init__(self):
        self.maxdepth = 3
        self.fl = '-'
    def heuristic(self):
        return 100 
    def update_lists(self,game_board, block_stat, move_ret, fl):

        game_board[move_ret[0]][move_ret[1]] = fl

        block_no = (move_ret[0]/3)*3 + move_ret[1]/3    
        id1 = block_no/3
        id2 = block_no%3
        mflg = 0

        flag = 0
        for i in range(id1*3,id1*3+3):
            for j in range(id2*3,id2*3+3):
                if game_board[i][j] == '-':
                    flag = 1

        if flag == 0:
            block_stat[block_no] = 'D'

        if block_stat[block_no] == '-':
            if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
            if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
                mflg=1
            if mflg != 1:
                        for i in range(id2*3,id2*3+3):
                            if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                    mflg = 1
                                    break
            if mflg != 1:
                        for i in range(id1*3,id1*3+3):
                            if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                    mflg = 1
                                    break
        if mflg == 1:
            block_stat[block_no] = fl
        
        return mflg    
        
    def alphabeta(self,temp_board,temp_block,old_move,depth,alpha,beta,maxpl):
        if depth==0 or self.terminal_state_reached(temp_board,temp_block)==True:
            return self.heuristic()
        ntemp_block = copy.deepcopy(temp_block)
        ntemp_board = copy.deepcopy(temp_board)
        blocks_allowed  = self.determine_blocks_allowed(old_move, ntemp_block)
        cells = self.get_empty_out_of(ntemp_board, blocks_allowed,ntemp_block)
        
        if maxpl:
            v = -1000
            for cell in cells:
                nntemp_board = copy.deepcopy(ntemp_board)
                nntemp_block = copy.deepcopy(ntemp_block)
                nntemp_board[cell[0]][cell[1]] = self.fl
                self.update_lists(nntemp_board,nntemp_block,cell,self.fl)
                v = max(v,aplhabeta(nntemp_board,nntemp_block,cell,depth-1,copy.deepcopy(alpha),copy.deepcopy(beta),False))
                alpha = max(alpha,v)
                if beta <= alpha:
                    break
                return v
        else:       
            v = 1000
            for cell in cells:
                nntemp_board = copy.deepcopy(ntemp_board)
                nntemp_block = copy.deepcopy(ntemp_block)
                nntemp_board[cell[0]][cell[1]] = self.fl
                self.update_lists(nntemp_board,nntemp_block,cell,self.fl)
                v = min(v,aplhabeta(nntemp_board,nntemp_block,depth-1,copy.deepcopy(alpha),copy.deepcopy(beta),False))
                beta = min(beta,v)
                if beta <= alpha:
                    break
                return v
            

    def terminal_state_reached(self,game_board, block_stat):
        ### we are now concerned only with block_stat
        bs = block_stat
        ## Row win
        if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
            return True
        ## Col win
        elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
            return True
        ## Diag win
        elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
            return True
        else:
            smfl = 0
            pl1 = 0
            for i in range(9):
                if block_stat[i] == '-':
                    smfl = 1
                    break
            if smfl == 1:
                return False
            else:
                return True

        

    def determine_blocks_allowed(self,old_move, block_stat):
        blocks_allowed = []
        if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
            blocks_allowed = [1,3]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
            blocks_allowed = [1,5]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
            blocks_allowed = [3,7]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
            blocks_allowed = [5,7]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
            blocks_allowed = [0,2]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
            blocks_allowed = [0,6]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
            blocks_allowed = [6,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
            blocks_allowed = [2,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
            blocks_allowed = [4]
        final_blocks_allowed = []
        for i in blocks_allowed:
            if block_stat[i]=='-':
                final_blocks_allowed.append(i)
        return final_blocks_allowed

    def get_empty_out_of(self,gameb, blal, block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	return cells
    
    def move(self, temp_board,temp_block,old_move, flag):
        #signal.signal(signal.SIGALRM, handler)
        #signal.alarm(TIMEALLOWED)
        self.fl = flag
        blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
        cells = self.get_empty_out_of(temp_board, blocks_allowed,temp_block)
        try:
            return cells[random.randrange(len(cells))]
        except:
            return cells[random.randrange(len(cells))]
        #signal.alarm(0)
