import graph_index_repo
from graph_index_repo import graph_index_repo
from opensearchpy import OpenSearch
import json

class opensearch_repo(graph_index_repo):

    os_client = None
    index = 'index-hgraph'
    
    def __init__(self):
        auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
        ca_certs_path = './root-ca.pem'
        self.os_client = OpenSearch(
                hosts = [{'host': 'opensearch-node1', 'port': 9200}],
                http_compress = True, 
                http_auth = auth,
                use_ssl = True,
                verify_certs = True,
                ssl_assert_hostname = False,
                ssl_show_warn = False,
                ca_certs = ca_certs_path
            )
        if(self.os_client.indices.exists(index=self.index == False)):
            index_body = {'settings': {'index': {'number_of_shards': 4}}}
            response = self.os_client.indices.create(self.index, body=index_body)
            print('\nCreating index:')
            print(response)

    def get(self, id: str ):
        try:
            value = self.os_client.get(index='index-hgraph', id=id, realtime=True)
            source = value['_source']
            to_nodes = source['to_nodes']
            return to_nodes
        except:
            return None

    
    def index(self, id: str, value: dict):
        jbody = { "from_node" : id, "to_nodes" : value}
        print("indexing : {}".format(jbody))
        return self.os_client.index(
            index = 'index-hgraph',
            body = jbody,
            id = id,
            refresh = True
        )

    def size(self):
        return 1838