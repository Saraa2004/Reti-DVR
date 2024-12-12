# Progetto Reti di Telecomunicazione, traccia 2

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = {name: 0}
    
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor.name] = cost

    def update_routing_table(self):
        updated = False

        for neighbor, cost in self.neighbors.items():
            for dest, curr_cost in neighbor.routing_table.items():
                new_cost = curr_cost + cost
                if dest not in self.routing_table or new_cost < self.routing_table[dest]:
                    self.routing_table[dest] = new_cost
                    updated = True
        return updated

    def __str__(self):
        result = f"\nTabella di routing per il nodo {self.name}:\n"
        result += "Destinazione | Costo\n"
        for dest, cost in sorted(self.routing_table.items()):
            result += f"     {dest}       |   {cost}\n"
        return result


class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        self.nodes[name] = Node(name);

    def add_link(self, node1_name, node2_name, cost):
        node1 = self.nodes[node1_name]
        node2 = self.nodes[node2_name]
        node1.add_neighbor(node2, cost)
        node2.add_neighbor(node1, cost)       

    def distance_vector_routing(self):
        converged = False
        iterations = 0

        while not converged:
            converged = True
            iterations += 1
            print(f"\n=== Iterazione {iterations} ===")
            for node in self.nodes.values():
                if node.update_routing_table():
                    converged = False
            
            for node in self.nodes.values():
                print(node)
        
        print(f"\nConvergenza dopo {iterations} iterazioni")


if __name__ == "__main__":
    network = Network()

    for node_name in ["A", "B", "C", "D", "E"]:
        network.add_node(node_name)
    
    network.add_link("A", "B", 2)
    network.add_link("B", "C", 3)
    network.add_link("C", "D", 1)
    network.add_link("D", "E", 5)
    network.add_link("A", "D", 1)
    network.add_link("A", "E", 1)
    network.add_link("B", "D", 2)
    network.add_link("C", "E", 4)

    network.distance_vector_routing()
