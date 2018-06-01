from set_algebra import Set


def do_bulk_xor_tests(tests):

    for x, y, expected in tests:
        X = Set(x)
        Y = Set(y)
        Z1 = X ^ Y

        assert Z1 == Set(expected), '%s ^ %s -> %s' % (X.notation, Y.notation, Z1.notation)

        Z2 = Y ^ X
        assert Z1 == Z2
        assert X == Set(x)
        assert Y == Set(y)


def test_xor_empty():

    tests = [
        ([], [], []),
        ([0], [], [0]),
        ([0, 1], [], [0, 1]),
        ('[0, 1]', [], '[0, 1]'),
        ('[0, 1], (2, 3)', [], '[0, 1], (2, 3)'),
        ('{0}, (1, 2)', [], '{0}, (1, 2)'),
        ('(0, 1), {2}', [], '(0, 1), {2}'),
    ]

    do_bulk_xor_tests(tests)


def test_xor_scalars():

    tests = [
        ([0], [0], []),
        ([0], [1], [0, 1]),
        ([0], [1, 2], [0, 1, 2]),
        ([1], [1, 2], [2]),
        ([2], [1, 2], [1]),
        (range(0, 10, 2), range(1, 10, 2), range(0, 10)),
    ]

    do_bulk_xor_tests(tests)


def test_xor_scalars_and_intervals():

    tests = [
        ('(0, 2)', [0, 1, 2], '[0, 1), (1, 2]'),
        ('[0, 1), (1, 2]', [0, 1, 2], '(0, 2)'),
        ('(0, 1), {2}, [3, 5], {6}', '(0, 6)', '[1, 2), (2, 3), (5, 6]'),
        (
            # 0   1   2   3   4   5   6   7
            # ----------------    .       .
            #     .   .   .       .    ---
            #  --- --- --- ---         ----
            '(0, 4), {5}, {7}',
            '{1}, {2}, {3}, {5}, (6, 7)',
            '(0, 1), (1, 2), (2, 3), (3, 4), (6, 7]'
        ),
        (
            # 0   1   2   3   4   5   6   7   8
            #     .   ---- ----   -------------
            # -----    ---------------        .
            # ----    .   .    ---    --------
            '{1}, [2, 3), (3, 4], [5, 8]',
            '[0, 1], (2, 6), {8}',
            '[0, 1), {2}, {3}, (4, 5), [6, 8)'
        ),
    ]

    do_bulk_xor_tests(tests)


def test_xor_intervals_unique_values():
    """Both Sets contain intervals only. All the endpoint values are unique."""

    tests = [
        (
            # 0   1   2   3   4   5   6   7   8   9
            # -----                           -----
            #          ---     ---     ---
            # -----    ---     ---     ---    -----
            '[0, 1], [8, 9]',
            '(2, 3), (4, 5), (6, 7)',
            '[0, 1], (2, 3), (4, 5), (6, 7), [8, 9]'
        ),
        (
            # 0   1   2   3
            # -------------
            #      ---
            # -----   -----
            '[0, 3]',
            '(1, 2)',
            '[0, 1], [2, 3]'
        ),
        (
            # 0   1   2   3   4   5
            #          -------
            # -----        -------
            # -----    ----   ----
            '(2, 4)',
            '[0, 1], (3, 5)',
            '[0, 1], (2, 3], [4, 5)'
        ),
        (
            # 0   1   2   3   4   5   6   7
            # -----------------------------
            #      ---     ---     ---
            # -----   -----   -----   -----
            '[0, 7]',
            '(1, 2), (3, 4), (5, 6)',
            '[0, 1], [2, 3], [4, 5], [6, 7]'
        ),
        (
            # 0   1   2   3   4   5   6   7
            # -----       -----    ---
            #         ---------------------
            # -----   ----     ----   -----
            '[0, 1], [3, 4], (5, 6)',
            '[2, 7]',
            '[0, 1], [2, 3), (4, 5], [6, 7]'
        ),
        (
            # 0   1   2   3   4   5   6   7   8   9
            # ---------   -------------   ---------
            #      ------------    ------------
            # -----    ---     ----    ---     ----
            '[0, 2], [3, 6], [7, 9]',
            '(1, 4], (5, 8]',
            '[0, 1], (2, 3), (4, 5], (6, 7), (8, 9]'
        ),    
        (
            # 0   1   2   3   4   5   6   7   8   9
            #             -----    ---    ---------
            # -----   -------------------------
            # -----   ----     ----   ----     ----
            '[3, 4], (5, 6), [7, 9]',
            '[0, 1], [2, 8]',
            '[0, 1], [2, 3), (4, 5], [6, 7), (8, 9]'
        ),
        (
            # 0   1   2   3   4   5   6   7   8   9   10
            #  -------         ----   ---------
            #      --------        -------         ---
            #  ----   -----    -------    -----    ---
            '(0, 2), (4, 5], [6, 8]',
            '(1, 3], (5, 7), (9, 10)',
            '(0, 1], [2, 3], (4, 6), [7, 8], (9, 10)'
        ),
        (
# 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19  20
# -----           - - -       -----           ------  ------  --------------
#          ---             -----------     -----------------------     ------------
#          |      |        |  |      |        |                   |        |
# -----    ---    - - -    ---     ---     ---      --      --    -----     -------
            '[0, 1], [4, 4.3], [4.4, 4.6], [4.7, 5], [7, 8], [11,12], [13,14], [15,18]',
            '(2, 3), (6, 9), (10, 16), (17, 20)',
            '[0, 1], (2, 3), [4, 4.3], [4.4, 4.6], [4.7, 5], (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), [16, 17], (18, 20)'
        ),
    ]

    do_bulk_xor_tests(tests)


def test_xor_bounding_intervals():
    """Both Sets contain intervals only. Some endpoint values are same."""

    tests = [
        ('[0, 1]', '[0, 1]', []),
        ('[0, 1]', '[0, 1)', '{1}'),
        ('[0, 1]', '(0, 1]', '{0}'),
        ('[0, 1]', '(0, 1)', '{0}, {1}'),
        ('[0, 1]', '[1, 2]', '[0, 1), (1, 2]'),
        ('[0, 1]', '(1, 2]', '[0, 2]'),
        ('[0, 1)', '[1, 2]', '[0, 2]'),

        ('[0, 1], [2, 3]', '(1, 2)', '[0, 3]'),
        ('[0, 1], [2, 3]', '[1, 2)', '[0, 1), (1, 3]'),
        ('[0, 1], [2, 3]', '(1, 2]', '[0, 2), (2, 3]'),
        ('[0, 1], [2, 3]', '[1, 2]', '[0, 1), (1, 2), (2, 3]'),

        ('[0, 1), [2, 3]', '(1, 2)', '[0, 1), (1, 3]'),
        ('[0, 1), [2, 3]', '[1, 2)', '[0, 3]'),
        ('[0, 1), [2, 3]', '(1, 2]', '[0, 1), (1, 2), (2, 3]'),
        ('[0, 1), [2, 3]', '[1, 2]', '[0, 2), (2, 3]'),

        ('[0, 1], (2, 3]', '(1, 2)', '[0, 2), (2, 3]'),
        ('[0, 1], (2, 3]', '[1, 2)', '[0, 1), (1, 2), (2, 3]'),
        ('[0, 1], (2, 3]', '(1, 2]', '[0, 3]'),
        ('[0, 1], (2, 3]', '[1, 2]', '[0, 1), (1, 3]'),

        ('[0, 1), (2, 3]', '(1, 2)', '[0, 1), (1, 2), (2, 3]'),
        ('[0, 1), (2, 3]', '[1, 2)', '[0, 2), (2, 3]'),
        ('[0, 1), (2, 3]', '(1, 2]', '[0, 1), (1, 3]'),
        ('[0, 1), (2, 3]', '[1, 2]', '[0, 3]'),

        ('[0, 1], [4, 5]', '(1, 2), (3, 4)', '[0, 2), (3, 5]'),
        ('[0, 1], [4, 5]', '[1, 2), (3, 4)', '[0, 1), (1, 2), (3, 5]'),
        ('[0, 1], [4, 5]', '(1, 2], [3, 4]', '[0, 2], [3, 4), (4, 5]'),
        ('[0, 1], [4, 5]', '[1, 2], [3, 4]', '[0, 1), (1, 2], [3, 4), (4, 5]'),

        ('(0, 2)', '(1, 2], [3, 4)', '(0, 1], {2}, [3, 4)'),
        ('[0, 1)', '(0, 2]', '{0}, [1, 2]'),
    ]

    do_bulk_xor_tests(tests)


def test_xor_inf():

    tests = [
        ('(-inf, inf)', [], '(-inf, inf)'),
        ('(-inf, inf)', [0], '(-inf, 0), (0, inf)'),
        ('(-inf, inf)', [0, 1], '(-inf, 0), (0, 1), (1, inf)'),
        ('(-inf, inf)', '(0, 1)', '(-inf, 0], [1, inf)'),
        ('(-inf, inf)', '(0, inf)', '(-inf, 0]'),
        ('(-inf, inf)', '(-inf, 0)', '[0, inf)'),
        ('(-inf, inf)', '(-inf, inf)', []),
        ('(-inf, 1)', '(0, inf)', '(-inf, 0], [1, inf)'),
        ('(-inf, 1)', '{0}, (1, inf)', '(-inf, 0), (0, 1), (1, inf)'),
    ]
    do_bulk_xor_tests(tests)

