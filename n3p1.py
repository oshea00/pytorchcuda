def n3p1(n):
    while n>1:
        print(n)
        if n%2 == 1:
            n = 3*n + 1
        else:
            n = n //2
    print(n)


# Converting APL code to python:  {(+⌿⍵)÷≢⍵}
def avg(x):
    return sum(x)/len(x)

# Convert APL code to python: (⍳10)∘.×⍳10
def mult_table():
    for i in range(1,11):
        for j in range(1,11):
            print(f"{i*j:>4}", end=" ")
        print()

# Convert APL code to python:
# {(⍵>0)/⍵}{≢¨1↓¨(1,~⍵∊⎕UCS 96+⍳26)⊂' ',⍵}
def lenwords(x):
    return [len(i) for i in x.split()]

print(avg([1,2,3,4,5]))
print(lenwords("to that list belongs only words with length greater than three"))
n3p1(27)
mult_table()

