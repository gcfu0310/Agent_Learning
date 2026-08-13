import numpy as np

# 两种方法计算余弦相似度,两种方法的输入可以是list也可以是np.array

# 方法一：手搓
def get_dot(vect_a,vect_b):
    if len(vect_a) != len(vect_b):
        raise ValueError

    sum_dot = 0
    for a,b in zip(vect_a,vect_b):
        sum_dot += a * b

    return sum_dot

def get_norm(vec):
    sum_norm = 0
    for num in vec:
        sum_norm += num * num
    return np.sqrt(sum_norm)

def cosine_similarity(vec_a,vec_b):
    return get_dot(vec_a,vec_b) / (get_norm(vec_a)*get_norm(vec_b))

# 方法二：numpy方法实现
def np_cosine_similarity(vec_a,vec_b):
    return np.dot(vec_a,vec_b) / (np.linalg.norm(vec_a)*np.linalg.norm(vec_b))

if __name__ == "__main__":
    A = [0.5,0.5,0.5]
    B = [0.7,0.7,0.7]
    C = [1,2,3]
    print(f"手搓AB:{cosine_similarity(A,B)}")
    print(f"npAB:{np_cosine_similarity(A,B)}")
    print(f"手搓AC:{cosine_similarity(A,C)}")
    print(f"npAC:{np_cosine_similarity(A,C)}")
