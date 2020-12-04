import database

def get_most_represented(n, excluded=[]):
    C,L = database.load_db_csv(n, excluded)
    print("\n".join(["ID: " + str(C[i][0]) + ", NAME: " + L[i] + ", COUNT: " + str(len(C[i][1].split(' '))) for i in range(n)]))