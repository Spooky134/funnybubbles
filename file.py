import numpy as np


def read(path):
    return np.loadtxt(path, skiprows=1, delimiter=',')


def single_write_cluster(cluster, direct):
    np.savetxt(direct + str(cluster.name) + '.csv', cluster.params(),
               fmt='%1.4f', delimiter=' | ', newline='\n' + '-' * 42 + '\n',
               header='| Nt | x | y | z | distances | differences |')


def multy_write_cluster(clusters, direct):
    for cl in clusters:
        single_write_cluster(cl, direct)


def single_write_cluster_size(cluster, direct):
    np.savetxt(direct + str(cluster.name) + '.csv',
               [cluster.expected_size()],
               fmt='%1.4f', delimiter=' | ', newline='\n' + '-' * 42 + '\n',
               header='|x_center|y_center|z_center| R1 | R2 | R3 | ')


def multy_write_cluster_size(clusters, direct):
    for cl in clusters:
        single_write_cluster_size(cl, direct)


def single_write(name, array, direct, header):
    np.savetxt(direct + name + '.csv', array,
               fmt='%1.4f', delimiter=' | ', newline='\n' + '-' * 42 + '\n',
               header=header)


def multy_write(array_of_name, array_of_array, direct, header):
    if len(array_of_name) == len(array_of_array):
        for name, array in zip(array_of_name, array_of_array):
            single_write(name, array, direct, header)
    else:
        print('array sizes doesnt match')

