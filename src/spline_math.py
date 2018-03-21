import os
import numpy as np

#################################################################
###                           ZERO                            ###
#################################################################

# нулевой столбец // 4x1
def make_zero4_column():
    return np.matrix([[0.], [0.], [0.], [0.]])

# нулевая матрица // 4x4
def make_zero4x4_matrix():
    zero_col = make_zero4_column()
    return np.concatenate((zero_col,zero_col,zero_col,zero_col), axis=1)


#################################################################
###                        T MATRIX                           ###
#################################################################
# T(x) значение функции в точке // 4x1
def make_T_column(point):
    x = point
    return np.matrix([[1.], [x], [x**2], [x**3]])

# T'(x) первая производная функции в точке // 4x1
def make_Td_column(point):
    x = point
    return np.matrix([[0.], [1.], [2*x], [3*(x**2)]])

# T''(x) вторая производная функции в точке // 4x1
def make_Tdd_column(point):
    x = point
    return np.matrix([[0.], [0.], [2.], [6*x]])


#################################################################
###                     A,B,C,D MATRIX                        ###
#################################################################
# Матрица A = [T(a), T(b), T'(b), T''(b)] // 4x4
def make_A_matrix(a_point, b_point):
    col1 = make_T_column(a_point)
    col2 = make_T_column(b_point)
    col3 = make_Td_column(b_point)
    col4 = make_Tdd_column(b_point)
    return np.concatenate((col1, col2, col3, col4), axis=1)

# Матрица B = [O, O, T'(a), T''(a)] // 4x4
def make_B_matrix(a_point):
    col1 = make_zero4_column()
    col2 = make_zero4_column()
    col3 = make_Td_column(a_point)
    col4 = make_Tdd_column(a_point)

    return np.concatenate((col1, col2, col3, col4), axis=1)

# Матрица C = [T(a_n), T(b1), O, T''(b_n)] // 4x4
# Hermite: C = [T(a_n), T(b1), O, T'(b_n)]
def make_C_matrix(a1, b1, an, bn, hermite=False):
    col1 = make_T_column(an)
    col2 = make_T_column(b1)
    col3 = make_zero4_column()
    col4 = make_Tdd_column(bn)
    if(hermite == True):
        col4 = make_Td_column(bn)
    return np.concatenate((col1, col2, col3, col4), axis=1)

# Матрица D = [O, O, -T''(a1), O] // 4x4
# Hermite: D = [O, O, -T'(a1), O]
def make_D_matrix(a1, hermite=False):
    col1 = make_zero4_column()
    col2 = make_zero4_column()
    col3 = make_Tdd_column(a1) * (-1)
    if(hermite == True):
        col3 = make_Td_column(a1) * (-1)
    col4 = make_zero4_column()
    return np.concatenate((col1, col2, col3, col4), axis=1)


#################################################################
###                        U MATRIX                           ###
#################################################################

# Строка U = [P_(i-1), P_i, O, O] // 2x4
# Hermite U = [P_(i-1),P_i, Vector1, Vector2]
def make_U_row(a_point, b_point, vector1 = None, vector2 = None):
    x1 = a_point[0]
    y1 = a_point[1]
    x2 = b_point[0]
    y2 = b_point[1]

    if (vector1 == None) or (vector2 == None):
        vector1 = [0., 0.]
        vector2 = [0., 0.]

    return np.matrix([[x1, x2, vector1[0], vector2[0]], [y1, y2, vector1[1], vector2[1]]])

# Матрица U = [U1, U2, ..., Un] // 2x4n
def make_U_matrix(source_points, vector1=None, vector2=None):
    U_matrix = make_U_row(source_points[0], source_points[1])

    points_num = len(source_points)
    for i in range(2, points_num-1):
        U_row = make_U_row(source_points[i-1], source_points[i])
        U_matrix = np.concatenate((U_matrix, U_row), axis=1)
    U_row = make_U_row(source_points[points_num-2], source_points[points_num-1], vector1, vector2)
    U_matrix = np.concatenate((U_matrix, U_row), axis=1)

    return U_matrix


#################################################################
###                        Q MATRIX                           ###
#################################################################

# Матрица Q // 4nx4n
def make_Q_matrix(source_points, hermite=False):
    interval_num = len(source_points) - 1

    Q_matrix = make_Q_raw(1, interval_num, source_points, hermite)
    for i_row in range(2, interval_num+1):
        Q_raw = make_Q_raw(i_row, interval_num, source_points, hermite)
        Q_matrix = np.concatenate((Q_matrix, Q_raw), axis=0)

    return Q_matrix

# Строка матрица Q // 4x4n
def make_Q_raw(idx, num, source_points, hermite=False):
    # ADD FIRST CELL
    Q_raw = make_zero4x4_matrix()
    if (idx == 1):
        Q_raw = make_A_matrix(0, 1)
    elif (idx == 2):
        Q_raw = make_B_matrix(0) * (-1)
    #print(Q_raw)

    # ADD CELL FROM 2 TO N-1
    for i in range(2, num):
        Q_el = make_zero4x4_matrix()
        if (i == idx):
            Q_el = make_A_matrix(0, 1)
        elif (i == (idx-1)):
            Q_el = make_B_matrix(0) * (-1)
        Q_raw = np.concatenate((Q_raw, Q_el), axis=1)
        #print(Q_raw)

    # ADD LAST CELL
    Q_el_last = make_zero4x4_matrix()
    if (idx == 1):
        Q_el_last = make_D_matrix(0, hermite) * (-1)
    elif (idx == num):
        Q_el_last = make_C_matrix(0, 1, 0, 1, hermite)
    Q_raw = np.concatenate((Q_raw, Q_el_last), axis=1)
    #print(Q_raw)

    return Q_raw


#################################################################
###                        S MATRIX                           ###
#################################################################
# S Matrix: free spline // 2x4n
def calculate_free_S_matrix(source_points):
    U_matrix = make_U_matrix(source_points)
    Q_matrix = make_Q_matrix(source_points)

    S_matrix = U_matrix * Q_matrix.I
    return S_matrix

# S Matrix: hermite pline // 2x4n
def calculate_hermite_S_matrix(source_points, vector1, vector2):
    U_matrix = make_U_matrix(source_points, vector1, vector2)
    print(U_matrix)
    Q_matrix = make_Q_matrix(source_points, hermite=True)

    S_matrix = U_matrix * Q_matrix.I
    return S_matrix


#################################################################
###                   S MATRIX COMPUTING                      ###
#################################################################
def get_points_from_S_matrix(S_matrix):
    x_polynomes_points = []
    y_polynomes_points = []

    for i in range(0, int(S_matrix[0].size/4)):
        sx0 = float(S_matrix[0, i * 4 + 0])
        sx1 = float(S_matrix[0, i * 4 + 1])
        sx2 = float(S_matrix[0, i * 4 + 2])
        sx3 = float(S_matrix[0, i * 4 + 3])

        x_arr = []
        for j in range(0, 100, 1):
            x = j * 0.01
            x_arr.append(sx0 + sx1 * x + sx2 * (x ** 2) + sx3 * (x ** 3))
        x_polynomes_points.append(x_arr)

        sy0 = S_matrix[1, i * 4 + 0]
        sy1 = S_matrix[1, i * 4 + 1]
        sy2 = S_matrix[1, i * 4 + 2]
        sy3 = S_matrix[1, i * 4 + 3]

        y_arr = []
        for j in range(0, 100, 1):
            y = j * 0.01
            y_arr.append(sy0 + sy1 * y + sy2 * (y ** 2) + sy3 * (y ** 3))
        y_polynomes_points.append(y_arr)

    return x_polynomes_points, y_polynomes_points


#################################################################
###                       GET SPLINE                          ###
#################################################################

def get_free_spline(source_points):
    S_matrix = calculate_free_S_matrix(source_points)
    return get_points_from_S_matrix(S_matrix)

def get_hermite_spline(source_points, vector1, vector2):
    S_matrix = calculate_hermite_S_matrix(source_points, vector1, vector2)
    return get_points_from_S_matrix(S_matrix)


# source = [[4.,0.],[0.,3.],[0.,0.]]
# calculate_hermite_S_matrix(source)

