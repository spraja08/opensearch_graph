import graph_index_repo
from graph_index_repo import graph_index_repo

class mem_repo(graph_index_repo):
    
    adj_matrix: dict = {}

    def get(self, id: str ):
        if id in self.adj_matrix:
            return self.adj_matrix[id]
        return None
    
    def index(self, id: str, value: dict):
        self.adj_matrix[id] = value

    def size(self):
        return len(self.adj_matrix)
