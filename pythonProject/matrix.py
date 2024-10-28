class Matrix:
    n: int
    m: int
    matrix: list[list]

    def __init__(self, n, m, matrix: list[list] = None):
        self.n = n
        self.m = m

        if matrix is None:
            self.matrix = [[0 for _ in range(m)] for _ in range(n)]
        else:
            if len(matrix) != n or any(len(row) != m for row in matrix):
                raise ValueError('Matrix dimensions do not match')
            self.matrix = matrix

    def get(self, i, j):
        if i < 0 or i >= self.n or j < 0 or j >= self.m:
            raise ValueError('Index out of bounds')
        return self.matrix[i][j]

    def set(self, i, j, value):
        if i < 0 or i >= self.n or j < 0 or j >= self.m:
            raise ValueError('Index out of bounds')
        self.matrix[i][j] = value

    def transpose(self):
        return Matrix(self.m, self.n, [list(col) for col in zip(*self.matrix)])

    def dot(self, other):
        if self.m != other.n:
            raise ValueError('Matrix dimensions do not match')

        result = []
        for i in range(self.n):
            row = []
            for j in range(other.m):
                row.append(sum(self.get(i, k) * other.get(k, j) for k in range(self.m)))
            result.append(row)
        return Matrix(self.n, other.m, result)

    def mutate(self, f: callable):
        for i in range(self.n):
            for j in range(self.m):
                self.set(i, j, f(self.get(i, j)))

    def __str__(self):
        return '\n'.join(' '.join(str(x) for x in row) for row in self.matrix)


matrix = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
print(matrix)
print("=====")
print(matrix.get(1, 2))
print("=====")
matrix.set(1, 2, 10)
print(matrix)
print("=====")
transposed = matrix.transpose()
print(transposed)
print("=====")
print(matrix.dot(transposed))
print("=====")
matrix.mutate(lambda x: x * 2)
print(matrix)
