from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

#Uses Gaussian elimination on a 3x3 user-inputted matrix
#to reduce to Reduced Row Echelon Form
def row_reduce(matrix):
    
    #Specify NumPy array
    matrix = np.array(matrix, dtype=float)
    rows, cols = matrix.shape

    #Row reduction
    for i in range(min(rows, cols)):
        if matrix[i][i] != 0:
            matrix[i] = matrix[i] / matrix[i][i]
        for j in range(rows):
            if j != i:
                matrix[j] = matrix[j] - matrix[j][i] * matrix[i]
    return matrix