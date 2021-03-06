"""Hard coded tables for butcher tableus containg
"a" butcher matrices
"b" weights
"c" abscissae

http://homepage.math.uiowa.edu/~ljay/publications.html
L.O. Jay: Lobatto methods. [online, .pdf]. Encyclopedia of Applied and
Computational Mathematics [.pdf], Numerical Analysis of Ordinary Differential
Equations, Springer - The Language of Science, Bj\"orn Engquist (Ed.), 2015.
"""

from math import sqrt

BUTCHER_TABLEU = {
    "lobatto_iiia": {
        "butcher_matrix": {
            2: [[0, 0], [1 / 2, 1 / 2]],
            3: [[0, 0, 0], [5 / 24, 1 / 3, -1 / 24], [1 / 6, 2 / 3, 1 / 6]],
            4: [
                [0, 0, 0, 0],
                [(a + b * sqrt(5)) / 120 for a, b in zip([11, 25, 25, -1], [1, -1, -13, 1])],
                [(a + b * sqrt(5)) / 120 for a, b in zip([11, 25, 25, -1], [-1, 13, 1, -1])],
                [1 / 12, 5 / 12, 5 / 12, 1 / 12],
            ],
        },
        "weights": {2: [1 / 2, 1 / 2], 3: [1 / 6, 2 / 3, 1 / 6], 4: [1 / 12, 5 / 12, 5 / 12, 1 / 12],},
        "abscissae": {2: [0, 1], 3: [0, 1 / 2, 1], 4: [0, 1 / 2 - sqrt(5) / 10, 1 / 2 + sqrt(5) / 10, 1],},
    },
    "lobatto_iiib": {
        "butcher_matrix": {
            2: [[1 / 2, 0], [1 / 2, 0]],
            3: [[1 / 6, -1 / 6, 0], [1 / 6, 1 / 3, 0], [1 / 6, 5 / 6, 0]],
            4: [
                [1 / 12, (-1 - sqrt(5)) / 24, (-1 + sqrt(5)) / 24, 0],
                [1 / 12, (25 + sqrt(5)) / 120, (25 - 13 * sqrt(5)) / 120, 0],
                [1 / 12, (25 + 13 * sqrt(5)) / 120, (25 - sqrt(5)) / 120, 0],
                [1 / 12, (11 - sqrt(5)) / 24, (11 + sqrt(5)) / 24, 0],
            ],
        },
        "weights": {2: [1 / 2, 1 / 2], 3: [1 / 6, 2 / 3, 1 / 6], 4: [1 / 12, 5 / 12, 5 / 12, 1 / 12],},
        "abscissae": {2: [0, 1], 3: [0, 1 / 2, 1], 4: [0, 1 / 2 - sqrt(5) / 10, 1 / 2 + sqrt(5) / 10, 1],},
    },
    "lobatto_iiic*": {
        "butcher_matrix": {2: [[0, 0], [1, 0]], 3: [[0, 0, 0], [1 / 4, 1 / 4, 0], [0, 1, 0]],},
        "weights": {2: [1 / 2, 1 / 2], 3: [1 / 6, 2 / 3, 1 / 6]},
        "abscissae": {2: [0, 1], 3: [0, 1 / 2, 1]},
    },
    "lobatto_iiic": {
        "butcher_matrix": {
            2: [[1 / 2, -1 / 2], [1 / 2, 1 / 2]],
            3: [[1 / 6, -1 / 3, 1 / 6], [1 / 6, 5 / 12, -1 / 12], [1 / 6, 2 / 3, 1 / 6],],
            4: [
                [1 / 12, -sqrt(5) / 12, sqrt(5) / 12, -1 / 12],
                [1 / 12, 1 / 4, (10 - 7 * sqrt(5)) / 60, sqrt(5) / 60],
                [1 / 12, (10 + 7 * sqrt(5)) / 60, 1 / 4, -sqrt(5) / 60],
                [1 / 12, 5 / 12, 5 / 12, 1 / 12],
            ],
            5: [
                [1 / 20, -7 / 60, 2 / 15, -7 / 60, 1 / 20],
                [1 / 20, 29 / 180, (47 - 15 * sqrt(21)) / 315, (203 - 30 * sqrt(21)) / 1260, -3 / 140,],
                [1 / 20, (329 + 105 * sqrt(21)) / 2880, 73 / 360, (329 - 105 * sqrt(21)) / 2880, 3 / 160,],
                [1 / 20, (203 + 30 * sqrt(21)) / 1260, (47 + 15 * sqrt(21)) / 315, 29 / 180, -3 / 140,],
                [1 / 20, 49 / 180, 16 / 45, 49 / 180, 1 / 20],
            ],
        },
        "weights": {
            2: [1 / 2, 1 / 2],
            3: [1 / 6, 2 / 3, 1 / 6],
            4: [1 / 12, 5 / 12, 5 / 12, 1 / 12],
            5: [1 / 20, 49 / 180, 16 / 45, 49 / 180, 1 / 20],
        },
        "abscissae": {  # node coefficients that multiply h, f(x+c*h)
            2: [0, 1],
            3: [0, 1 / 2, 1],
            4: [0, 1 / 2 - sqrt(5) / 10, 1 / 2 + sqrt(5) / 10, 1],
            5: [0, 1 / 2 - sqrt(21) / 14, 1 / 2, 1 / 2 + sqrt(21) / 14, 1],
        },
    },
}
