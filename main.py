# Progetto Reti di Telecomunicazione, Sara Panfini

"""
La classe Node rappresenta un nodo all'interno della rete.
Ogni nodo ha 
- un nome, che lo identifica
- una lista di vicini, con associativi i relativi costi dei collegamenti
- una tabella di routing, per tenere traccia dei percorsi migliori per raggiungere gli altri nodi
"""

class Node:

    # Inizializzazione di un nodo
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.routing_table = {name: 0} # La distanza di ogni nodo da se stesso è pari a zero.
    
    """
    Aggiunge un vicino alla lista dei nodi vicini e modifica la tabella di routing iniziale.
    """
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost
        self.routing_table[neighbor.name] = cost

    """
    Aggiorna la tabella di routing usando l'algoritmo Distance Vector Routing.
    Confronta le informazioni relative ai costi dei collegamenti con gli altri nodi 
    presenti nella tabella di routing del nodo in esame con quelle ricevute dai nodi vicini.
    Se viene trovato un percorso con un costo minore rispetto a quello registrato nella tabella di routing, la tabella viene aggiornata.
    Il metodo ritorna True se la tabella è stata aggiornata, False altrimenti.
    """
    def update_routing_table(self):
        updated = False

        for neighbor, cost in self.neighbors.items():
            for dest, curr_cost in neighbor.routing_table.items():
                new_cost = curr_cost + cost
                if dest not in self.routing_table or new_cost < self.routing_table[dest]:
                    self.routing_table[dest] = new_cost
                    updated = True
        return updated

    """
    Rappresenta in maniera chiara la tabella di routing del nodo in formato stringa.
    """
    def __str__(self):
        result = f"\nTabella di routing per il nodo {self.name}\n"
        result += "Destinazione | Costo\n"
        for dest, cost in sorted(self.routing_table.items()):
            result += f"     {dest}       |   {cost}\n"
        return result

"""
La classe Network rappresenta l'intera rete di nodi.
Permette di aggiungere nodi e collegamenti e di simulare il 
protocollo di routing DVR per calcolare le tabelle di routing dei nodi.
"""

class Network:

    # Inizializzazione di una rete vuota
    def __init__(self):
        self.nodes = {}

    """
    Aggiunge un nuovo nodo alla rete.
    """
    def add_node(self, name):
        self.nodes[name] = Node(name);

    """
    Aggiunge un nuovo collegamento tra due nodi in entrambe le direzioni e con un costo specifico.
    """
    def add_link(self, node1_name, node2_name, cost):
        node1 = self.nodes[node1_name]
        node2 = self.nodes[node2_name]
        node1.add_neighbor(node2, cost)
        node2.add_neighbor(node1, cost)       

    """
    Simula il funzionamento dell'algoritmo DVR fino alla convergenza delle tabelle.
    """
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
        
        print(f"Convergenza dopo {iterations} iterazioni")

if __name__ == "__main__":

    # Esempio di creazione di una rete per effettuare la simulazione.

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

    # Esecuzione dell'algoritmo DVR
    network.distance_vector_routing()
