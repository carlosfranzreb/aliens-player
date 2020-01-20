"""
Test different values for the offset of the shooting, to optimise it.
"""


from aliens import main
from multiprocessing import Process, Manager


def multi_test(n, player):
    procs = []
    manager = Manager()
    return_list = manager.list()
    for _ in range(n):
        proc = Process(target=multi_child, args=(player, return_list,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    return sum(return_list) / len(return_list)


def multi_child(player, return_list):
    return_list.append(main(player))
    return return_list


if __name__ == '__main__':
    res = multi_test(1, "computer")
    print(res)
