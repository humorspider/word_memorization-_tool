import random

def split_point(sum_num, k):
    # Generate k - 1 random integers
    rand_nums = []
    for i in range(k - 1):
        rand = random.randint(0, sum_num)
        rand_nums.append(rand)
        sum_num -= rand

    # Calculate the last integer
    rand_nums.append(sum_num)

    # Output the result
    return rand_nums

# 测试示例
total = 10
count = 4
result = split_point(total, count)
print(result)
