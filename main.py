from constants import SBox, c, CFault1, CFault2, CFault3

def sub_bytes(byte):
    return SBox[byte // 16][byte % 16]

def calcul_delta(C, CFault) :
    return C ^ CFault

def calcul_key_schedule_faulted(x, epsilon):
    return sub_bytes(x) ^ sub_bytes(x ^ epsilon)


def find_X(C, CFault):
    epsilon = 1 # 0x01
    matches = []
    for x in range(256):
        for i in range(8):
            if calcul_delta(C, CFault) == calcul_key_schedule_faulted(x, epsilon):
                matches += [format(x, 'x')]
            
            epsilon *= 2 # epsilon = epsilon << 1 (shift left)

        epsilon = 1 # reset epsilon
    
    return matches

def find_key(X, C):
    return sub_bytes(X) ^ C

if __name__ == '__main__':
    # Find the key
    list1 = find_X(c, CFault1)
    list2 = find_X(c, CFault2)
    list3 = find_X(c, CFault3)

    # Find the intersection of the 3 lists
    intersection_list = list(set(list1) & set(list2) & set(list3))

    print("Possible keys:", intersection_list) # normally only one key
    print("Most probable X:", intersection_list[0])

    k10 = find_key(int(intersection_list[0], 16), c) 
    print(f"Key: 0x{k10:02X} ")