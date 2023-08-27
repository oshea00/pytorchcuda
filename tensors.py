import torch
import numpy as np

data = [[1,2],[3,4]]
x_data = torch.tensor(data)

np_array = np.array(data)
x_np = torch.from_numpy(np_array)

x_rand = torch.rand_like(x_data, dtype=torch.float)


print(x_rand)

print(f"Shape of tensor: {x_rand.shape}")
print(f"Datatype of tensor: {x_rand.dtype}")
print(f"Device tensor is stored on: {x_rand.device}")

if torch.cuda.is_available():
    x_rand = x_rand.to('cuda')
    print(f"Device tensor is stored on: {x_rand.device}")


t1_columnwise = torch.cat([x_rand,x_rand], dim=1)
t1_columnwise[:,0] = 1
print(t1_columnwise)

print(x_rand.sin())

data = [[1.0,2.0],[3.0,4.0]]
t2  = torch.tensor(data)
print(t2 @ t2)
print(t2.det())
print(t2.inverse())
print(t2.inverse() @ t2)