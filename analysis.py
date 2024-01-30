import ast
import matplotlib.pyplot as plt

file_path = 'time.txt'

with open(file_path, 'r') as file:
    content = file.read().rstrip(',\n')

data = ast.literal_eval(content)

x_values, y_values = zip(*data)

plt.bar(x_values, y_values, width=0.8)
plt.xlabel('Request number')
plt.ylabel('Execution time')
plt.grid(True)
plt.show()
