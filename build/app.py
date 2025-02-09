from flask import Flask, render_template, request
import numpy as np
from fractions import Fraction

app = Flask(__name__)

#Uses Gaussian elimination on a 3x3 user-inputted matrix
#to reduce to Reduced Row Echelon Form
def row_reduce(matrix):
    
    #Sets matrix to a list of fractions
    matrix = [[Fraction(x) for x in row] for row in matrix]
    rows, cols = len(matrix), len(matrix[0])

    #Row reduction
    for i in range(min(rows, cols)):
        if matrix[i][i] != 0:
            matrix[i] = [x / matrix[i][i] for x in matrix[i]]
        for j in range(rows):
            if j != i:
                matrix[j] = [matrix[j][k] - matrix[j][i] * matrix[i][k] for k in range(cols)]
    return matrix

#Solves the system of equations, handling cases with 0, 1, or infinite solutions
def solve(matrix):
    solutions = {}
    rows = len(matrix)
    cols = len(matrix[0])

    if any(row[-1] and not any(row[:-1]) for row in matrix):
        return None  #Checks if matrix is inconsistent, if there's an all 0 row except the last column
    
    # unique solutions cases
    for i in range(rows):
        pivot_col = -1
        for j in range(cols - 1):
            if matrix[i][j] != 0:
                pivot_col = j
                break
        if pivot_col != -1:
            solutions[pivot_col] = matrix[i][-1] - sum(
                matrix[i][j] * solutions.get(j, 0) for j in range(pivot_col + 1, cols - 1)
            )

    # infinitely many solutions case
    for j in range(cols - 1):
        if j not in solutions:
            solutions[j] = f"free (let x{j+1} = t)"

    return solutions



@app.route('/', methods = ['GET', 'POST'])

def index():
    if request.method == 'POST':
        #Get matrix and call row_reduce
        #Store the reduced matrix in matrix_reduced
        matrix = [
            [Fraction(request.form['a11']), Fraction(request.form['a12']), Fraction(request.form['a13']), Fraction(request.form['b1'])],
            [Fraction(request.form['a21']), Fraction(request.form['a22']), Fraction(request.form['a23']), Fraction(request.form['b2'])],
            [Fraction(request.form['a31']), Fraction(request.form['a32']), Fraction(request.form['a33']), Fraction(request.form['b3'])]
        ]
        matrix_reduced = row_reduce(matrix)
        solutions = solve(matrix_reduced)
        return render_template('index.html', matrix=matrix, matrix_reduced=matrix_reduced, solutions = solutions) 
    return render_template('index.html', matrix=None, matrix_reduced=None, solutions = None) #Set matrix to empty when app is first loaded

if __name__ == '__main__':
    app.run(debug=True) 