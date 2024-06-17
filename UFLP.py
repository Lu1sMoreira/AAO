import numpy as np


# Função para carregar os dados do arquivo cap71.txt
def carregar_dados(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Parâmetros do problema
    m, n = map(int, lines[0].split())
    print(f"m = {m}, n = {n}")

    # Capacidades e custos fixos
    capacities = []
    fixed_costs = []
    for i in range(1, m + 1):
        capacity, fixed_cost = map(float, lines[i].split())
        capacities.append(capacity)
        fixed_costs.append(fixed_cost)

    print(f"Capacities: {len(capacities)}")
    print(f"Fixed Costs: {len(fixed_costs)}")

    # Demandas e custos de alocação
    demands = []
    allocation_costs = []
    i = m + 1
    while i < len(lines):
        if len(lines[i].split()) == 1:
            demands.append(int(lines[i].split()[0]))
            i += 1
        else:
            allocation_costs.append(list(map(float, lines[i].split())))
            i += 1

    print(f"Demands: {len(demands)}")
    print(f"Allocation Costs: {len(allocation_costs)}")

    return m, n, capacities, fixed_costs, demands, allocation_costs


# Função GRASP para resolver o UFLP
def grasp_uflp(m, n, capacities, fixed_costs, demands, allocation_costs, iterations=100):
    best_solution = None
    best_cost = float('inf')

    for _ in range(iterations):
        # Construção da solução inicial
        solution = []
        total_cost = 0

        # Passo guloso e aleatorizado
        for j in range(n):
            costs = [fixed_costs[i] + allocation_costs[j][i] for i in range(m)]
            sorted_indices = np.argsort(costs)
            selected = sorted_indices[np.random.randint(len(sorted_indices))]
            solution.append(selected)
            total_cost += costs[selected]

        # Busca local
        improved = True
        while improved:
            improved = False
            for j in range(n):
                current = solution[j]
                for i in range(m):
                    if i != current:
                        new_cost = total_cost - (fixed_costs[current] + allocation_costs[j][current]) + (
                                    fixed_costs[i] + allocation_costs[j][i])
                        if new_cost < total_cost:
                            solution[j] = i
                            total_cost = new_cost
                            improved = True

        # Atualização da melhor solução
        if total_cost < best_cost:
            best_cost = total_cost
            best_solution = solution

    return best_solution, best_cost


# Carregar os dados
m, n, capacities, fixed_costs, demands, allocation_costs = carregar_dados('cap71.txt')

# Verificar se os dados foram carregados corretamente
print("Dados carregados:")
print(f"Capacities: {capacities}")
print(f"Fixed Costs: {fixed_costs}")
print(f"Demands: {demands}")
print(f"Allocation Costs: {[len(costs) for costs in allocation_costs]}")

# Resolver o problema
best_solution, best_cost = grasp_uflp(m, n, capacities, fixed_costs, demands, allocation_costs)
print("Melhor solução:", best_solution)
print("Custo total:", best_cost)
