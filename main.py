import random
import pandas as pd
from haversine import haversine
import math
from operator import itemgetter

def pass_through(a):
    return a

def sin(a):
    return math.sin(a)

def cos(a):
    return math.cos(a)

def add(coeff1, func1, x, coeff2, func2, y):
    return coeff1 * func1(x) + coeff2 * func2(y)

def subtract(coeff1, func1, x, coeff2, func2, y):
    return coeff1 * func1(x) - coeff2 * func2(y)

def multiply(coeff1, func1, x, coeff2, func2, y):
    return (coeff1 * func1(x)) * (coeff2 * func2(y))

def divide(coeff1, func1, x, coeff2, func2, y):
    # Protected division
    if y == 0:
        if x > 0:
            return 1000000
        elif x < 0:
            return -1000000
    else:
        return (coeff1 * func1(x)) / (coeff2 * func2(y))

def operators(x, y):
    operator = ['o+', 'o-', 'o*', 'o/']
    functions = ['o', 'o', 'o', 'o', 'o', 'o', 'c', 's']
    coefficients = ['e0', 'e1', 'e2', 'e3', 'e4']
    return random.choice(coefficients) + random.choice(functions) + x + random.choice(operator) + random.choice(coefficients) + random.choice(functions) + y

#initialization
def initialize(n_programs):
    program_list_with_fitness = []
    max_program_length = 8

    input_registers = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']#,'14', '15']
    calculation_registers = ['a0', 'a1', 'a2']
    output_registers = ['o0', 'o1']
    constants = ['c0', 'c1', 'c2', 'c3', 'c4']
    total_list = input_registers + calculation_registers + output_registers + constants

    program_length = random.randint(1, max_program_length)

    for i in range(n_programs):
        program = []
        for i in range(program_length + 2):
            instruction = []
            if i < program_length:
                instruction.append(random.choice(calculation_registers + output_registers))
            elif i <= program_length:
                instruction.append(output_registers[0])
            else:
                instruction.append(output_registers[1])
            instruction.append(operators(random.choice(total_list), random.choice(total_list)))
            program.append(instruction)
        program_list_with_fitness.append([program, -1])
    return program_list_with_fitness

def evaluate(program_list_with_fitness):
    df = pd.read_csv('dataset.csv')
    df_ev = pd.read_csv('dataset_ev.csv')
    #df = pd.read_csv('final_dataset_20154.csv')
    #df_ev = pd.read_csv('for_evaluation.csv')

    for i, program_with_fitness in enumerate(program_list_with_fitness):
        fitness = program_with_fitness[1]
        program = program_with_fitness[0]

        if fitness != -1:
            continue

        ambulances = [x for x in range(1,33)]
        # ambulance_dict[amb identifying num] gives you [current_amb_count, (lat, long of the relocation suggested with that row's information)
        ambulance_dict = {ambulance:[0, (0,0)] for ambulance in ambulances}
        program_total_distance = 0

        for j, row in df.iterrows():
            # initialize calc and output registers as 1
            rs = {}
            rs['a0'] = 1
            rs['a1'] = 1
            rs['a2'] = 1
            rs['o0'] = 1
            rs['o1'] = 1

            # set input registers to the feature values
            rs['01'] = df.iloc[j, 0]
            rs['02'] = df.iloc[j, 1]
            rs['03'] = df.iloc[j, 2]
            rs['04'] = df.iloc[j, 3]
            rs['05'] = df.iloc[j, 4]
            rs['06'] = df.iloc[j, 5]
            rs['07'] = df.iloc[j, 6]
            rs['08'] = df.iloc[j, 7]
            rs['09'] = df.iloc[j, 8]
            rs['10'] = df.iloc[j, 9]
            rs['11'] = df.iloc[j, 10]
            rs['12'] = df.iloc[j, 11]
            rs['13'] = df.iloc[j, 12]

            # initialize constants
            rs['c0'] = 1
            rs['c1'] = 2
            rs['c2'] = 3
            rs['c3'] = 4
            rs['c4'] = 5

            # initialize coefficients
            rs['e0'] = 1
            rs['e1'] = 2
            rs['e2'] = 3
            rs['e3'] = 4
            rs['e4'] = 5

            # initialize functions
            rs['o'] = pass_through
            rs['s'] = sin
            rs['c'] = cos

            for instruction in program:
                right = instruction[1]
                arguments = rs[right[:2]], rs[right[2:3]], rs[right[3:5]], rs[right[7:9]], rs[right[9:10]], rs[right[10:]]
                op = instruction[1][5:7]
                if op == 'o+':
                    rs[instruction[0]] = add(*arguments)
                elif op == 'o-':
                    rs[instruction[0]] = subtract(*arguments)
                elif op == 'o*':
                    rs[instruction[0]] = multiply(*arguments)
                else: # op == 'o/'
                    rs[instruction[0]] = divide(*arguments)

            current_amb_count = ambulance_dict[df_ev.at[j, 'AMRVEHNUM']][0]
            if current_amb_count > 0:
                previous_row_relocation_coords = ambulance_dict[df_ev.at[j, 'AMRVEHNUM']][1]
                current_row_destination_coords = (df_ev.at[j, 'DESTLAT'], df_ev.at[j, 'DESTLONG'])
                program_total_distance += haversine(previous_row_relocation_coords, current_row_destination_coords)
            # program relocation coordinates = ambulance_dict[df_ev.at[j, 'AMRVEHNUM']][1]
            latitude = rs['o0'] % 0.14 + 39.95      # honed in on boulder latitude
            longitude = rs['o1'] % 0.16 - 105.15    # honed in on boulder longitude
            ambulance_dict[df_ev.at[j, 'AMRVEHNUM']][1] = (latitude, longitude)
            ambulance_dict[df_ev.at[j, 'AMRVEHNUM']][0] += 1

        print(program_total_distance)
        program_list_with_fitness[i] = [program, program_total_distance]
    #print(df_ev['DISTANCE'].sum() - df_ev.at[0, 'DISTANCE'])

    return program_list_with_fitness

def selection(program_list_with_fitness, program_list_length, top_proportion):
    num_selected = math.ceil(program_list_length * top_proportion)

    sorted_program_list_with_fitness = sorted(program_list_with_fitness, key=itemgetter(1))
    top_performers = sorted_program_list_with_fitness[:num_selected]

    return top_performers

def recombination(top_performers, n_offspring):
    # Determine random mating pairs
    # num of offspring is equal to num of survivors
    pairs = []
    children = []
    for i in range(n_offspring):
        pairs.append(random.sample(top_performers, 2))

    # Mating - generate 1 offspring per pair using one point crossover
    for pair in pairs:
        len_list = [len(pair[0][0]), len(pair[1][0])]
        len_list.sort()
        crossover_index = random.randint(0, len_list[0])

        children.append([pair[0][0][:crossover_index] + pair[1][0][crossover_index:], -1])
    return children

def mutation(children, mutation_rate):
    n_children = len(children)
    n_children_mutated = math.ceil(mutation_rate * n_children)

    register_choices = ['a0', 'a1', 'a2', 'o0', 'o1',
                        '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',# '14', '15',
                        'c0', 'c1', 'c2', 'c3', 'c4']

    for mutation in range(n_children_mutated):
        child = random.choice(children)
        instruction = random.choice(child[0])
        register_position_choice = random.randint(1, 2)      # o0 = c4 + r3 .... only one of the last two registers are changed
        if register_position_choice == 1:
            instruction[1] = instruction[1][:3] + random.choice(register_choices) + instruction[1][5:]
        else:
            instruction[1] = instruction[1][:10] + random.choice(register_choices)

    return children

def survival(program_list_with_fitness, n_survivors):
    sorted_program_list_with_fitness = sorted(program_list_with_fitness, key=itemgetter(1))
    survivors = sorted_program_list_with_fitness[:n_survivors]

    return survivors

def main():
    top_proportion = 0.2
    bottom_proportion = 0.2
    n_programs = 50
    n_generations = 1000
    n_survivors = math.ceil(n_programs * bottom_proportion)
    mutation_rate = 10       # num of mutations (e.g. a single register, constant) per individual

    # Make n_programs of random programs
    program_list_with_fitness = initialize(n_programs)

    # Evaluate the population on fitness (i.e. distance between relocation point and next call location)
    program_list_with_fitness = evaluate(program_list_with_fitness)
    program_list_length = len(program_list_with_fitness)

    for i in range(n_generations):
        print('Generation ' + str(i))
        # Identify highest fitness programs - parents
        top_performers = selection(program_list_with_fitness, program_list_length, top_proportion)

        # Breed parents, form children
        children = recombination(top_performers, n_survivors)

        # Mutate children
        children = mutation(children, mutation_rate)

        # Add children to population
        program_list_with_fitness = program_list_with_fitness + children

        # Evaluate population on fitness
        program_list_with_fitness = evaluate(program_list_with_fitness)

        # Terminate bottom performing programs
        program_list_with_fitness = survival(program_list_with_fitness, n_survivors)

        print(program_list_with_fitness)

main()