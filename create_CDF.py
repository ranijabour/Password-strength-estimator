import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import PESrank_new
import PESrank


def plot(file, country, title, top_values):
    data = []
    cnt = 0
    with open(file, "r") as file:
        for line in file:
            cnt += 1
            if cnt > 5000:
                break
            if line:
                line = line.strip()
                if title != "particular":
                    rank, exp = PESrank.main(line, os.getcwd())
                    data.append(rank)
                else:
                    rank, exp, ind = PESrank_new.main(line, os.getcwd(), top_values, country=country)
                    data.append(rank)
    data.sort()
    return data


def compute_cdf(data, bin_edges):
    # Compute histogram
    hist, _ = np.histogram(data, bins=bin_edges)

    # Calculate the CDF
    cdf = np.cumsum(hist) / len(data) * 100
    return cdf


def create_CDF(test_file, country):
    dict_result = {}

    # Define a list of 'n' values for experimentation.
    for n in ["100", "1000", "5000"]:
        # Load data for 'n' from specific contexts.
        start_time1 = time.time()
        data1 = plot(test_file, country, "particular", n)
        end_time1 = time.time()
        start_time2 = time.time()
        data2 = plot(test_file, country, "general", n)
        end_time2 = time.time()
        execution_time1 = end_time1 - start_time1
        execution_time2 = end_time2 - start_time2
        dict_time[n] = [execution_time2, execution_time1]
        avg_1 = (sum(data1)) / (len(data1))
        avg_2 = (sum(data2)) / (len(data2))
        dict_result[n] = [avg_1, avg_2, avg_1 - avg_2]
    
        # Create a logarithmic histogram for the data.
        bin_edges = np.logspace(0, 24, num=int(1E24 / 1E21) + 1)
        cdf1 = compute_cdf(data1, bin_edges)
        cdf2 = compute_cdf(data2, bin_edges)

        # Generate a comparative plot.
        plt.figure(figsize=(8, 6))
        plt.semilogx(bin_edges[:-1], cdf1, linestyle='--', color='blue', linewidth=1.2, label='With Context')
        plt.semilogx(bin_edges[:-1], cdf2, linestyle='-', color='red', linewidth=1.2, label='Without Context')
        plt.xlabel('Number of Attempts')
        plt.ylabel('Crackability (%)')
        plt.grid(True, which="both", ls="--", c='0.8')
        plt.yticks(np.arange(0, 110, 10))
        plt.ylim(0, 100)
        plt.legend(loc='lower right', fontsize='medium')
        plt.tight_layout(pad=2.0)
        plt.title(f'{country}(Top-{n})')
        plt.savefig(f'{country}_{n}.png', dpi=300)
        
    return dict_result, dict_time
