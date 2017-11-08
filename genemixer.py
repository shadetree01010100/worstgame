import random
import struct


def float_to_bin(f):
    ba = struct.pack('>f', f)
    s = ''.join('{:08b}'.format(b) for b in ba)
    return s

def bin_to_float(b):
    bf = int_to_bytes(int(b, 2), 4)
    return struct.unpack('>f', bf)[0]

def int_to_bytes(n, minlen=0):
    nbits = n.bit_length() + (1 if n < 0 else 0)
    nbytes = (nbits + 7) // 8
    b = bytearray()
    for _ in range(nbytes):
        b.append(n & 0xff)
        n >>= 8
    # zero padding
    if minlen and len(b) < minlen:
        b.extend([0] * (minlen - len(b)))
    return bytearray(reversed(b))

def mix_genes(a, b, mutation_rate=0.01, output=False):
    a_dna = float_to_bin(a)
    b_dna = float_to_bin(b)
    donor_genes = zip(a_dna, b_dna)
    genes = []
    mutations = []
    for gene_pair in donor_genes:
        gene = random.choice(gene_pair)
        if random.random() < mutation_rate:
            gene = str(abs(int(gene) - 1))
            mutations.append('V')
        else:
            mutations.append('-')
        genes.append(gene)
    genes[1] = '0' # prevent inf/nan by fixing this gene at 0, blame IEEE
    # todo: fixed point arithmatic
    offspring_dna = ''.join(genes)
    offspring = bin_to_float(offspring_dna)
    if output:
        print('a: ', a_dna, ' ' if a > 0 else '', a)
        print('b: ', b_dna, ' ' if b > 0 else '', b)
        print('   ', ''.join(mutations))
        print('   ',
            offspring_dna,
            ' ' if offspring > 0 else '',
            offspring)
        print('=' * 79)
    return offspring

if __name__ == '__main__':
    # test
    import os
    os.system('cls')
    print('')
    for _ in range(10):
        donor_a = random.gauss(0, 1)
        donor_b = random.gauss(0, 1)
        mix_genes(donor_a, donor_b, output=True)
