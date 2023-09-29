from copy import copy, deepcopy
from utils import *
from Global import Matrix
import numpy as np
import pandas as pd

colums_header = []
listNone = []
paresCaminos = []
index_center_star = None


def saveTxt(df):
    with open('output.txt', mode='w') as file_object:
        print("Matrix de Score:\n", file=file_object)
        print(df, file=file_object)


def saveStartTXT(center_string, index_center_star, pares_alignment, multiple_alignment):
    f = open("output.txt", "a")
    f.write("Cadena central: " + center_string + '\n')
    f.write("Indice de la cadena central: " + str(index_center_star) + '\n')
    f.write("\nAlineaciones con la cadena central:\n")

    for i in pares_alignment:
        f.write(i + "\n")

    f.write("\nAlinieación Multiple\n")
    for i in multiple_alignment:
        f.write(i + "\n")

def consistency(string_center, aligments):
    len_aligs = list(map(lambda alig: len(alig), aligments))
    max_len = max(len_aligs)
    all_string = [string_center] + aligments
    multiple_aligments = []
    for old_alig in all_string:
        amount_to_fill = max_len - len(old_alig)
        new_alig = old_alig + ("-" * amount_to_fill)
        multiple_aligments.append(new_alig)
    return multiple_aligments


def MatrixScoreAllString(list_inputs):
    n_string = len(list_inputs)
    matrix_score = np.full(shape=(n_string, n_string), fill_value=0).tolist()
    matrix_MatrixGlobal = []
    matrix_alignments = np.full(shape=(n_string, n_string), fill_value="").tolist()
    for n in range(len(list_inputs)):
        matrix_MatrixGlobal.append(listNone)

    for i in range(n_string):
        for j in range(i + 1, n_string):
            s1, s2 = list_inputs[i], list_inputs[j]
            MatrixGlobal = Matrix(s1, s2)
            matrix_alignments[i][j] = MatrixGlobal.getFistAlignment()

            MatrixGlobalMirror = Matrix(s2, s1)
            matrix_alignments[j][i] = matrix_alignments[i][j]

            matrix_MatrixGlobal[i][j] = MatrixGlobal
            matrix_MatrixGlobal[j][i] = MatrixGlobalMirror
            matrix_score[i][j] = matrix_MatrixGlobal[i][j].score
            matrix_score[j][i] = matrix_score[i][j]
        print("+" * 10)
    print(matrix_alignments)
    df = pd.DataFrame(data=matrix_score, columns=colums_header, index=colums_header)
    df['Sum'] = df.sum(axis=1)
    saveTxt(df)
    print(df)
    df = df.reset_index()
    index_center_star = df['Sum'].idxmax()
    print("String centro es el orden: ", index_center_star + 1)

    row_paths = matrix_alignments[index_center_star]
    # print("Alineamientos con centro:", row_paths)
    del row_paths[index_center_star]
    string_center = list_inputs[index_center_star]
    print("Centro:", string_center)
    print("Alineamientos sin centro:", row_paths)
    print(string_center)
    for row in row_paths:
        print(row)
    aligments = consistency(string_center, row_paths)
    saveStartTXT(string_center, index_center_star, row_paths, aligments)




if __name__ == '__main__':
    list_inputs, colums_header = readInputs()
    for i in range(len(list_inputs)):
        listNone.append(None)
    MatrixScoreAllString(list_inputs)
    
