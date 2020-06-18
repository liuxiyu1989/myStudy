import numpy as np

# 测试numpy的基本用法
def test_numpy():
    array = np.array([(1, 0, 1, 2, 3, 4), (1, 2, 3, 4, 5, 6)], np.int)
    print(array.ndim)
    print(array.shape)
    print(array.size)


if __name__ == '__main__':
    # test_numpy()
    # array = np.zeros((4,5),np.int)
    # print(array)
    # print(np.ones((3,3),np.float))
    arr1 = np.arange(0,20,1)
    # print(arr1)
    # print(np.arange(0, 12, 1).reshape((3, 4)))
    # print(np.linspace(0, 20, 4).reshape((2,2)))
    # print(np.linspace(0, 20, 16).reshape(-1, 8))
    # array1 = np.array([[1, 2.0], [1.9, 3.4]])
    # array2 = np.array([[3.6, 1.2], [2.0, 1.2]])
    # print(array1)
    # print(array2)
    # print(array1 * array2)
    # print(np.dot(array1, array2))
    # print(np.log1p(1))
    # np.log1p()
    # np.save('data',arr1)
    # arr2 =np.load("data.npy")
    # print(arr2)
    # print(np.where([[False, True ,False], [False, True,False],[False,True,False]],
    #          [[5, 3,1], [7, 9,2],[10,11,3]],
    #          [[2, 6,4], [1, 8,5],[12,13,6]]))
    # np.savetxt('text.out',arr1,delimiter=',')
    a = np.arange(12)
    a.shape=(3,4)
    print(a)
    #resize方法影响的是本身不是赋值给b
    b = a.resize([2,6])

    print (b)
    print(a)
    c = np.concatenate((a,a,a),axis = 0)
    print(c)
    d = np.cos(a)
    print(d)
    print(np.pi/2)
    np.cos
    print(np.cos(np.pi/2))
    print(np.pi)
    ################################################
    f = 'd'
    arr = np.loadtxt('D:/1.txt',delimiter=',',usecols= np.arange(3),dtype= np.int)
    print(arr)
    print(arr.shape)
    print(arr.dtype)
    print(np.linalg.norm(arr,ord= np.inf))
    print(-np.inf)









