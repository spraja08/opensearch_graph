from collections import deque
from csv import DictReader
from functools import wraps
import json
from opensearch_repo import opensearch_repo
from opensearchpy import OpenSearch
from pickle import NONE
import time

from mem_repo import mem_repo
from mock_graph_data import edges

class Graph:

    def __init__(self, repo_type: str):
        if( repo_type == 'memdb'):
            self.repo = mem_repo()
            self.load_test_data(edges)
        elif( repo_type == 'opensearch' ):
            self.repo = opensearch_repo()

    repo = None

    def timeit(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            total_time_str = f'{total_time:.4f}'
            print(f'Function {func.__name__}{args} {kwargs} Took {total_time_str} seconds')
            return result, total_time_str
        return timeit_wrapper


    def get_leaf(self, radial_graph: dict, paths: list[str]):
        for path in paths:
            leaf = radial_graph[path]
            radial_graph = leaf
        return leaf

    def load_graph_data(self, path: str):
        with open(path, 'r') as read_obj:
            csv_reader = DictReader(read_obj)
            header = next(csv_reader)
            if header is not None:
                for row in csv_reader:
                    key = row['entity_from_guid']
                    value = self.repo.get(key)
                    if value is not None:
                        value.append(row['entity_to_guid'])
                    else:
                        value = [row['entity_to_guid']]
                    self.repo.index(key, value)
        print("loaded {} entries".format(self.repo.size()))

    def load_test_data(self, testData: list[list[int]]):
        for row in testData:
            key = str(row[0])
            value = str(row[1])
            existing_value = self.repo.get(key)
            if existing_value is not None:
                existing_value.append(value)
            else:
                existing_value = [value]
            self.repo.index(key, existing_value)
        print("loaded {} entries".format(self.repo.size()))

    def get_all_connections(self, node: str):
        return self.repo.get(node)

    def printpath(self, path: list[int]) -> None:
        size = len(path)
        for i in range(size):
            print(path[i], end=" ")
        print()

    @timeit
    def get_radial_data(self, source: str, degrees: int):
        queue = deque()
        radial_graph = { source : {}}
        queue.append([source].copy())

        while queue:
            path = queue.popleft()
            if(len(path)) > degrees + 1:
                continue
            leaf_to_add: dict = self.get_leaf(radial_graph, path)
            last_node = path[-1]
            connections = self.get_all_connections(last_node)
            if(connections is not None):
                for connection in connections:
                    if (connection not in path):
                        leaf_to_add[connection] = {}
                        new_partial_path = path.copy()
                        new_partial_path.append(connection)
                        queue.append(new_partial_path)
        return radial_graph

    @timeit
    def get_all_paths(self, source: str, destination: str, degrees: int) -> list[list[str]]:
        if(source == destination):
            return [[source, destination]]
        if(self.repo.get(id=source) == None):
            return [[]]

        queue = deque()
        all_paths = []
        queue.append([source].copy())

        while queue:
            path = queue.popleft()
            if(len(path)) > degrees:
                continue
            lastNode = path[-1]

            if(lastNode == destination):
                all_paths.append(path)

            connections = self.get_all_connections(lastNode)
            if(connections != None):
                for connection in connections:
                    if (connection not in path):
                        new_partial_path = path.copy()
                        new_partial_path.append(connection)
                        queue.append(new_partial_path)
        return all_paths
