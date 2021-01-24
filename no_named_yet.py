import pandas as pd

x = pd.DataFrame([1,2,3])
y = pd.DataFrame([1,2,3])

print(x.shape)
print(y.shape)

print(type(x))
print(type(y))


print(x.dot(y.T).melt())
