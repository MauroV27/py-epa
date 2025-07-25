from random import random
import copy

POS_MAP = [[-1, 3, -1], [2, -1, 5], [-1, 7, -1]]
CLOSE_GRID : float = 0.92

class EntropyPropagration : 
    
    sizeW : int
    sizeH : int

    def __init__(self):
        pass    

    @staticmethod
    def setGridSize(w:int, h:int) -> None:
        EntropyPropagration.sizeW = w
        EntropyPropagration.sizeH = h


    @staticmethod
    def generate_matrix(n_w:int, n_h:int) -> list:
        # Criar uma matriz n x n preenchida com 0
        matrix = [] # for energy values
        

        matrix_row = [[0, 0] for _ in range(n_h)]  
        matrix = [copy.deepcopy(matrix_row) for _ in range(n_w)]   
        
        return matrix


    @staticmethod
    def propagate_energy(matrix:list, x:int, y:int, energy:int) -> int:
        # nw = len(matrix)
        # nh = len(matrix[0])
        nw = EntropyPropagration.sizeW
        nh = EntropyPropagration.sizeH

        # Verificar se as coordenadas estão dentro da matriz
        if x < 0 or x >= nw or y < 0 or y >= nh:
                return 0

        # Verificar se a energia já foi propagada para essa posição
        if energy <= 0:
                return 0
        
        if matrix[x][y][0] > 0 and random() < CLOSE_GRID :
                return 0
            
        # chance da casa n existir
        if random() > (energy/4) + 0.5:
                return 0

        matrix[x][y][0] = 1 # Atribuir a energia à posição atual
        v = energy

        # Propagar a energia para as casas vizinhas
        a = EntropyPropagration.propagate_energy(matrix, x-1, y, energy-1)  # left
        b = EntropyPropagration.propagate_energy(matrix, x+1, y, energy-1)  # right
        c = EntropyPropagration.propagate_energy(matrix, x, y-1, energy-1)  # up
        d = EntropyPropagration.propagate_energy(matrix, x, y+1, energy-1)  # down

        EntropyPropagration.cells_around(x, y, x-1, y, a, matrix)
        EntropyPropagration.cells_around(x, y, x+1, y, b, matrix)
        EntropyPropagration.cells_around(x, y, x, y-1, c, matrix)
        EntropyPropagration.cells_around(x, y, x, y+1, d, matrix)

        matrix[x][y][0] = v + a + b + c + d
        return matrix[x][y][0]

    @staticmethod
    def cells_around(x, y, lx, ly, value, level) -> None:
        if value == 0:
                return
        
        values = EntropyPropagration.multply_around(x, y, lx, ly)
        if values[0] == -1 or values[1] == -1:
                return
        
        if level[x][y][1] == 0:
                level[x][y][1] = 1

        if value >= 1 and level[lx][ly][1] < 1:
                level[lx][ly][1] = 1

        vxy = level[x][y][1] * values[1]
        vlxly = level[lx][ly][1] * values[0]
        
        if EntropyPropagration.verify_factor(vxy) and EntropyPropagration.verify_factor(vlxly):
                level[x][y][1] = vxy
                level[lx][ly][1] = vlxly

    @staticmethod
    def is_valid_modular_factor(value:int, m:int) -> bool:
        if value <= m or value % m == 1:
                return True
        
        return value % (m*m) >= 1
    

    @staticmethod
    def verify_factor(value:int) -> bool:
        m2 = EntropyPropagration.is_valid_modular_factor(value, 2)
        m3 = EntropyPropagration.is_valid_modular_factor(value, 3)
        m5 = EntropyPropagration.is_valid_modular_factor(value, 5)
        m7 = EntropyPropagration.is_valid_modular_factor(value, 7)
        
        return  m2 and m3 and m5 and m7
        

    @staticmethod
    def multply_around(x:int, y:int, lx:int, ly:int) -> list[int]:
        dx = x - lx + 1
        dy = y - ly + 1

        if dx == 0 or dx == 2:
                return [POS_MAP[dx][dy], POS_MAP[2-dx][dy]]
        if dy == 0 or dy == 2:
                return [POS_MAP[dx][dy], POS_MAP[dx][2-dy]]

        return [-1, -1]