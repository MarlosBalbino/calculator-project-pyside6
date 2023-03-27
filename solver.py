from copy import deepcopy

D = [[4,  2,   1, -2],
     [3, -3,  -1, -1],
     [3,  5,   1,  1],
     [1, -1,  -1,  4]]


I = [ 3, 
      2, 
      0, 
     -2]


class LinearSolver:
    solutions = []
    def cramer(self, D: list, I: list):

        size = len(D)
        det_D = self.laplace(D)

        if not det_D:
            return

        for j in range(size):
            M = deepcopy(D)
            for i in range(size):
                M[i][j] = I[i]

            solution = self.laplace(M) / det_D
            print(f"{solution:.4}")
            self.solutions.append(solution)

    def laplace(self, M):
        if len(M) < 3:
            return (M[0][0] * M[1][1]) - (M[0][1] * M[1][0])
        
        sum = 0
        for i in range(len(M)):
            M_aux = self.complementary(M, i)
            sum += (-1)**(i+2) * M[i][0] * self.laplace(M_aux)

        return sum

    @staticmethod
    def complementary(M, i):
        M_aux = [lin[1:] for lin in M]
        M_aux.pop(i)
        return M_aux

    @staticmethod
    def print_matrix(M):
        for lin in M:
            for a in lin:
                print(str(a).rjust(2, " "), end=" ")
            print()
        print()

    def get_solutions(self) -> list:
        return self.solutions


def read_matrix():

    num = int(input("Número de variáveis do seu sistema:\n"))

    print("\nDigite sua matriz (coeficientes dependentes:")
    D = []
    for _ in range(num):
        line = [float(a) for a in input().split()]
        D.append(line)

    print("\nDigite os coeficientes independentes:")
    I = [float(a) for a in input().split()]
    
    print("\nSoluções:\n")
    solver = LinearSolver()
    solver.cramer(D, I)


if __name__ == "__main__":
    read_matrix()

    





    





    
    

