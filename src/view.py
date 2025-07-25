import timeit
import matplotlib.pyplot as plt
import numpy as np
import copy
import platform
import sys
import math
import os
import psutil  # Importa a biblioteca psutil
import pandas as pd
from PIL import Image, ImageDraw

from src.algoritm import CLOSE_GRID, EntropyPropagration

import random

# Define um valor de seed (você pode escolher qualquer número inteiro)
seed_value = 42

# Bloqueia a seed do random
random.seed(seed_value)

process = psutil.Process(os.getpid())

class EntropyPropagrationPrint(EntropyPropagration) : 
    @staticmethod
    def propagate_energy(matrix: list, x: int, y: int, energy: int, frames: list):
        """
        Função de propagação de energia modificada para capturar os frames da animação.
        """
        nw = len(matrix[0])
        nh = len(matrix)
        
        # Condição de parada: fora da matriz
        if x < 0 or x >= nh or y < 0 or y >= nw:
            return 0
        
        # Condição de parada: energia esgotada
        if energy <= 0:
            return 0
        
        # Chance de parar se a célula já foi visitada (tem energia)
        if matrix[x][y][0] > 0 and random.random() < CLOSE_GRID:
            return 0
            
        # Chance de a célula "não existir" (propagação falha)
        if random.random() > (energy / 4) + 0.5:
            return 0

        # --- Início da Modificação e Captura ---
        matrix[x][y][0] = 1  # Atribui energia inicial
        v = energy
        
        # Captura o estado da matriz após a ativação inicial da célula
        frames.append(copy.deepcopy(matrix))

        # Propagação recursiva para os vizinhos
        a = EntropyPropagrationPrint.propagate_energy(matrix, x-1, y, energy-1, frames)
        b = EntropyPropagrationPrint.propagate_energy(matrix, x+1, y, energy-1, frames)
        c = EntropyPropagrationPrint.propagate_energy(matrix, x, y-1, energy-1, frames)
        d = EntropyPropagrationPrint.propagate_energy(matrix, x, y+1, energy-1, frames)

        EntropyPropagration.cells_around(x, y, x-1, y, a, matrix)
        EntropyPropagration.cells_around(x, y, x+1, y, b, matrix)
        EntropyPropagration.cells_around(x, y, x, y-1, c, matrix)
        EntropyPropagration.cells_around(x, y, x, y+1, d, matrix)

        matrix[x][y][0] = v + a + b + c + d

        frames.append(copy.deepcopy(matrix))
        
        return matrix[x][y][0]


class InputDataType:
    def __init__(self, width: int, height: int, x: int, y: int, energy: int):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.energy = energy

def entropy_ropagration_algoritm(inpt:InputDataType, frames):
    
    matrix = EntropyPropagrationPrint.generate_matrix(inpt.width, inpt.height)
    EntropyPropagrationPrint.propagate_energy(matrix, inpt.x, inpt.y, inpt.energy, frames)

    return frames

def get_color_from_energy(energy: int, max_energy: int) -> tuple:
    if energy == 0:
        return (10, 10, 20) 
    
    # Normaliza a energia para o intervalo [0, 1]
    # ratio = min(energy  / max_energy, 0.0)
    ratio = np.sin((energy/max_energy) )
    
    # Interpolação linear simples entre azul e amarelo

    r = int(128 + (128 * ratio))
    g = int(128 + (128 * ratio))
    b = int(128 + (128 * (1 - ratio)))
    
    return (r, g, b)

def create_propagation_gif_with_pillow(
        frames: list,
        filename: str = "benchmark/entropy_propagation_evolution.gif",
        cell_size: int = 10,
        duration: int = 50
    ):
    
    if not frames:
        print("Nenhum frame foi gerado. O GIF não será criado.")
        return

    pil_images = []
    
    # Acha a energia máxima para normalizar as cores consistentemente
    max_energy = max(cell[0] for frame in frames for row in frame for cell in row if cell[0] > 0)
    if max_energy == 0: max_energy = 1 # Evita divisão por zero

    print(f"Gerando GIF com {len(frames)} frames usando Pillow...")

    for frame_data in frames:
        width = len(frame_data[0])
        height = len(frame_data)
        
        # Cria uma nova imagem para este frame, com o tamanho escalado
        img = Image.new('RGB', (width * cell_size, height * cell_size))
        draw = ImageDraw.Draw(img)
        
        for r, row in enumerate(frame_data):
            for c, cell in enumerate(row):
                energy = cell[0]
                color = get_color_from_energy(energy, max_energy)
                
                # Define as coordenadas do retângulo para esta célula
                top_left_x = c * cell_size
                top_left_y = r * cell_size
                bottom_right_x = top_left_x + cell_size
                bottom_right_y = top_left_y + cell_size
                
                # Desenha o retângulo preenchido com a cor da energia
                draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], fill=color)
                
        pil_images.append(img)

    print(f"Salvando o arquivo GIF em '{filename}'...")
    # Salva a lista de imagens como um GIF animado
    pil_images[0].save(
        filename,
        save_all=True,
        append_images=pil_images[1:],
        duration=duration,  # Duração de cada frame em milissegundos
        loop=0,             # 0 para loop infinito
        optimize=True
    )
    print("GIF salvo com sucesso com Pillow! ✅")

def view_main():
    # Parâmetros de entrada para o algoritmo
    input_data = InputDataType(
        width=30,       # Largura da matriz
        height=30,      # Altura da matriz
        x=15,           # Posição X inicial
        y=15,           # Posição Y inicial
        energy=90       # Energia inicial (um pouco maior para um efeito mais visível)
    )
    
    # 1. Executa o algoritmo para obter a lista de frames (nenhuma mudança aqui)
    evolution_frames = entropy_ropagration_algoritm(input_data, [])
    
    # 2. Gera e salva o GIF usando a nova função baseada em Pillow
    create_propagation_gif_with_pillow(
        evolution_frames, 
        cell_size=16,    # Tamanho de cada célula em pixels no GIF final
        duration=30      # Duração de cada frame em ms (mais baixo = mais rápido)
    )


if __name__ == "__main__":
    view_main()