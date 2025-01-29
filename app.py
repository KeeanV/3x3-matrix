from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def row_reduce(matrix):
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape

    for i in range(min(rows, cols)):
        if matrix[i][i] != 0:
            matrix[i] = matrix[i] / matrix[i][i]
        for j in range(rows):
            if j != i:
                matrix[j] = matrix[j] - matrix[j][i] * matrix[i]
    return matrix