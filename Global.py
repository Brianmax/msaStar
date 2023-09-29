import numpy as np
import networkx as nx
from utils import KeepWay

class ValueCondition:
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __str__(self):
        return self.value


def bool_list(way):
    index = way[0]
    list_bool = []
    way = way[1::]

    for i, next_node in enumerate(way):
        index_diagonal = (index[0] - 1, index[1] - 1)
        if index_diagonal == next_node:
            list_bool.append(1)
        else:
            list_bool.append(0)
        index = next_node
    return list_bool


class Matrix:
    value_interval = -2  # gap
    values_matrix = None  # scores
    matrix_coordinates = None
    ways = None
    string1 = None
    string2 = None
    score = None

    def __init__(self, string1, string2, debug=False):
        self.G = nx.DiGraph()
        self.ways = []

        self.string1 = string1
        self.string2 = string2
        n, m = len(string1) + 1, len(string2) + 1
        self.debug = debug
        self.values_matrix = np.zeros((n, m), int)
        self.values_matrix[0] = np.arange(m) * self.value_interval
        self.values_matrix[:, 0] = np.arange(n) * self.value_interval

        self.matrix_coordinates = []
        for i in range(n):
            self.matrix_coordinates.append([])

        for i in range(m):
            tuple_index = (0, i - 1)
            self.matrix_coordinates[0].append([tuple_index])
        for i in range(1, n):
            tuple_index = (i - 1, 0)
            self.matrix_coordinates[i].append([tuple_index])
        self.matrix_coordinates[0][0] = [()]


    def travel_matrix(self, matrix, x, y):
        if x == 0 and y == 0:
            return 0

        amount_tuples = len(matrix[x][y])
        for i in range(amount_tuples):
            self.travel_matrix(matrix, matrix[x][y][i][0], matrix[x][y][i][1])
            self.G.add_edge((x, y), matrix[x][y][i])

    def create_graph(self, matrix):
        x_start = len(matrix) - 1
        y_start = len(matrix[0]) - 1
        self.score = self.values_matrix[x_start][y_start]
        self.travel_matrix(matrix, x_start, y_start)

    def fun(self, string1, string2):
        n, m = len(string1) + 1, len(string2) + 1

        for i in range(1, n):
            for j in range(1, m):
                value_first_condition = 1
                if string1[i - 1] != string2[j - 1]:
                    value_first_condition = -1

                index_1, index_2, index_3 = (i - 1, j - 1), (i - 1, j), (i, j - 1)
                value_1 = self.values_matrix[i - 1][j - 1]
                value_2 = self.values_matrix[i - 1][j]
                value_3 = self.values_matrix[i][j - 1]

                values_matrix = [ValueCondition(value_1 + value_first_condition, index_1),
                                 ValueCondition(value_2 - 2, index_2),
                                 ValueCondition(value_3 - 2, index_3)]
                sorted_values_conditions = sorted(values_matrix, key=lambda x: x.value)
                sorted_values_conditions.reverse()
                sorted_values_conditions = KeepWay(sorted_values_conditions)
                list_value_indexs = [classValue.index for classValue in sorted_values_conditions]

                self.matrix_coordinates[i].append(list_value_indexs)
                self.values_matrix[i][j] = sorted_values_conditions[0].value

        self.create_graph(self.matrix_coordinates)
        if self.debug:
            print("Matrix de Valores:", self.values_matrix)
            print("Matrix de Coordenadas:", self.matrix_coordinates)

    def alignments(self, string1, string2):
        n, m = len(string1) + 1, len(string2) + 1

        for path in nx.all_simple_paths(self.G, source=(n - 1, m - 1), target=(0, 0)):
            self.ways.append(path)

        if self.debug:
            print("Caminos para las alineaciones:", self.ways)

    def getAlignment(self, list_bool):
        list_bool.reverse()
        stringAlignment = ""
        i = 0
        i_s2 = 0
        max_string = self.string1
        min_string = self.string2
        if len(self.string2) > len(self.string1):
            max_string, min_string = self.string2, self.string1

        while i < len(max_string):
            if i_s2 == len(self.string1) - 1 and i_s2 != len(self.string2) - 1:
                for j in range(i_s2, len(self.string2)):
                    stringAlignment += self.string2[i_s2]

            elif i_s2 == len(self.string2) - 1:
                for j in range(i_s2, len(self.string2)):
                    stringAlignment += self.string2[i_s2]
                len_stringAlig = len(stringAlignment)
                len_string1 = len(self.string1)
                if len_stringAlig != len_string1 and len_string1 > len_stringAlig:
                    fill_gap = len_string1 - len_stringAlig
                    for j in range(0, fill_gap):
                        stringAlignment += "-"
                break
            elif list_bool[i] == 1:
                stringAlignment += self.string2[i_s2]
                i_s2 += 1
            else:
                stringAlignment += "-"
            i += 1

        return stringAlignment

    def saveTXT(self):
        np.savetxt('output.txt', self.values_matrix, fmt='%.0f', header="Matrix de Valores:")
        f = open("output.txt", "a")
        n, m = len(self.string1), len(self.string2)
        f.write("Score: " + str(self.values_matrix[n, m]) + '\n')
        f.write("Cantidad de alineamientos: " + str(len(self.ways)) + "\n")
        f.write("Alineamientos: " + "\n")
        for i in range(len(self.ways)):
            list_bool_to_alignment = bool_list(self.ways[i])
            alignment = self.getAlignment(list_bool_to_alignment)
            f.write(self.string1)
            f.write("\n")
            f.write(alignment)
            f.write("\n")
            f.write("-" * 10)
            f.write("\n")
        f.close()

    def getFistAlignment(self):

        self.fun(self.string1, self.string2)
        self.alignments(self.string1, self.string2)
        list_bool_to_alignment = bool_list(self.ways[0])
        print("Cantidad de Caminos:", len(self.ways))
        print("list_bool_to_alignment antes del get:", list_bool_to_alignment)
        alignment = self.getAlignment(list_bool_to_alignment)
        print(self.string1)
        print(alignment)
        print("*" * 10)

        return alignment
