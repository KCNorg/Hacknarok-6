def algos(V, D, R, alfa, LIMIT):
    n = len(V)
    visited = [False] * n
    T = [0, 2]
    visited[0] = True
    visited[2] = True


    curr_cost = sum([ D[T[i]][T[(i + 1) % len(T)]] for i in range(len(T))])
    curr_value = sum([V[i] for i in T])
    while curr_cost < LIMIT and not all(visited):
        R = alfa * (curr_value / curr_cost) + (1 - alfa) * R
        cost = -1000000
        min_node = -1
        between = -1
        for j in range(n):
            if visited[j]:
                continue
            for i in range(len(T)):
                delta_T = D[T[i]][j] + D[j][T[(i + 1)%len(T)]] - D[T[i]][T[(i + 1)%len(T)]]
                if V[j] - R*delta_T > cost:
                    cost = V[j] - R*delta_T
                    min_node = j
                    between = i

        visited[min_node] = True
        T.insert(between + 1, min_node)
        curr_cost = sum([D[T[i]][T[(i + 1) % len(T)]] for i in range(len(T))])
        curr_value = sum([V[i] for i in T])

    print(T)
    return T

