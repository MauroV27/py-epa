import timeit
import matplotlib.pyplot as plt
import numpy as np
import platform
import sys
import math
import os
import psutil  
import pandas as pd
from src.algoritm import EntropyPropagration

import random

from src.big_matrix import load_matrix

# Define um valor de seed 
SEED_VALUE = 42

# Bloqueia a seed do random
random.seed(SEED_VALUE)

process = psutil.Process(os.getpid())


class InputDataType:
    def __init__(self, width: int, height: int, x: int, y: int, energy: int):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.energy = energy



def entropy_ropagration_algoritm(inpt:InputDataType):
    
    matrix = load_matrix()
    EntropyPropagration.setGridSize(inpt.width, inpt.height)
    result = EntropyPropagration.propagate_energy(matrix, inpt.x, inpt.y, inpt.energy)

    return result


def another_algorithm(input_data):
    # Example of another algorithm for comparison
    return [x * 2 for x in range(input_data)]


def generate_odd_numbers(k: int) -> list[int]:
    odd_numbers = []
    number = 1
    while len(odd_numbers) < k:
        odd_numbers.append(number)
        number += 2
    return odd_numbers



def stores_data_for_test():

    
    number_of_executions = 100
    maps_sizes_for_experience = generate_odd_numbers(number_of_executions)

    inputs = []

    for size in maps_sizes_for_experience:
        center = size // 2
        energy = size
        inputs.append(InputDataType(width=size, height=size, x=center, y=center, energy=energy)) 


    all_times = [] 
    algorithm_times_mean = []
    algorithm_times_std = []
    memory_usages = []

    for inpt in inputs:
        times = timeit.repeat(lambda: entropy_ropagration_algoritm(inpt), repeat=number_of_executions, number=1)
        all_times.append(times) # Armazena todos os tempos
        algorithm_times_mean.append(np.mean(times))
        algorithm_times_std.append(np.std(times))
        mem_before = process.memory_info().rss
        # Execute novamente para medir a memória no mesmo ponto da execução
        timeit.repeat(lambda: entropy_ropagration_algoritm(inpt), repeat=1, number=1)
        mem_after = process.memory_info().rss
        memory_usages.append(mem_after - mem_before)


    # Cria os dados para a tabela
    data = {
        'width': [inpt.width for inpt in inputs],
        'height': [inpt.height for inpt in inputs],
        'x': [inpt.x for inpt in inputs],
        'y': [inpt.y for inpt in inputs],
        'energy': [inpt.energy for inpt in inputs],
        'average_execution_time': algorithm_times_mean,
        'std_dev_execution_time': algorithm_times_std, # Adicionada a coluna de desvio padrão
        'memory_usage_bytes': memory_usages
        # 'average_execution_time': algorithm_times,
        # 'memory_usage_bytes': memory_usages  # Adiciona a coluna de uso de memória
    }

    # Cria um DataFrame do pandas
    df = pd.DataFrame(data)

    # Salva o DataFrame em um arquivo CSV
    output_filename = 'benchmark/benchmark_results-test.csv'
    df.to_csv(output_filename, index=False)  # index=False para não salvar o índice do DataFrame

    print(f"Os resultados do benchmark foram salvos em '{output_filename}'")

    generate_graph(inputs ,algorithm_times_mean)

    # Imprimindo informações do ambiente (opcional)
    print("\nEnvironment Information:")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print(f"CPU: {platform.processor()}")




def generate_graph(inputs, algorithm_times) :

    # Cria os dados para a tabela e o gráfico
    energies = [inpt.energy for inpt in inputs]

    # Gera o gráfico
    plt.figure(figsize=(10, 6))
    plt.scatter(energies, algorithm_times, marker='o')
    # plt.plot( x_curve, y_curve, linestyle='-', color='red', label='O(n log n)')
    plt.xlabel('Energy')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Average Execution Time vs. Energy')
    plt.grid(True)

    # Salva a imagem do gráfico
    output_filename_png = 'benchmark/benchmark_plot_energy_time.png'
    plt.savefig(output_filename_png)
    print(f"O gráfico de tempo de execução vs. energia foi salvo em '{output_filename_png}'")


if __name__ == "__main__":
    stores_data_for_test()
        