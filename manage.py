from ezCLI import*

def manage():
    name = ['name']
    x = ['X_axis']
    y = ['Y_axis']
    angle = ['rotaion in degres']
    matrix = [name, angle, x, y]
    print(matrix)
    write_csv('graphy/premium/store.csv', matrix)

if __name__=='__main__':
    manage()