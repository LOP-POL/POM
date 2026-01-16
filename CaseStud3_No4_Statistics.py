# Monthly yield comparision of three shelf models
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

yieldComparison = {
    "Month": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Shelf 1": [
        49.970, 48.592, 49.346, 51.114, 49.177, 49.230,
        51.347, 50.728, 51.333, 49.631, 50.396, 50.757
    ],
    "Shelf 2": [
        65.631, 80.648, 85.449, 65.596, 52.317, 76.643,
        0.040, 62.098, 42.191, 117.399, 43.722, 108.916
    ],
    "Shelf 3": [
        77.480, 19.619, 73.747, 122.436, 170.719, 49.498,
        123.699, 64.830, 62.643, 87.862, 9.462, 3.138
    ]
}

df = pd.DataFrame(yieldComparison)

def getShelfValues(shelf):
    return df[shelf].tolist()

def calcMean(values):
    return round(sum(values) / len(values),3)

def calcPopStandardDeviation(values):
    mean = calcMean(values)
    return round(sqrt(sum((x - mean) ** 2 for x in values) / len(values)),3)

def calcSampleStandardDeviation(values):
    mean = calcMean(values)
    return round(sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1)),3)

def plotBellCurve(shelf):
    values = getShelfValues(shelf)
    mean = calcMean(values)
    std_dev = calcPopStandardDeviation(values)
    x = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 100)
    y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
    plt.plot(x, y, label=f'Bell Curve for {shelf}')

def plotHistogram(shelf, subplot):
    months = df["Month"].tolist()
    values = getShelfValues(shelf)
    subplot.bar(months, values, alpha=0.7, label=shelf, edgecolor='black')
    subplot.set_xlabel('Month')
    subplot.set_ylabel('Yield')
    subplot.set_title(f'{shelf}')
    subplot.legend()

# Main function to print results and plot
if __name__ == "__main__":
    # fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for idx, shelf in enumerate(["Shelf 1", "Shelf 2", "Shelf 3"]):
        values = getShelfValues(shelf)
        mean = calcMean(values)
        pop_std_dev = calcPopStandardDeviation(values)
        sample_std_dev = calcSampleStandardDeviation(values)
        print(f"{shelf} - Mean: {mean}, Population Std Dev: {pop_std_dev}, Sample Std Dev: {sample_std_dev}")
        
        # plotHistogram(shelf, axes[idx])
        plotBellCurve(shelf)

    plt.xlabel('Yield')
    plt.ylabel('Probability Density')
    plt.title('Bell Curves for All Shelves')
    plt.legend()
    plt.tight_layout()
    plt.show()
    