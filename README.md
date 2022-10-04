# Graph Algorithms using OpenSearch as Repo

OpenSearch and Dashboards will run in docker container.
The code indexes relationships data on OpenSearch and implements the following 2 algorithms

1. Given a start node, retrieve the Graph of connected nodes with n degrees 
2. Given a start and destination node, retrive all paths with n degrees of separation

# Getting started

1. Clone the repo
2. `docker-compose up -d`
3. `Usage - Radial search: http://localhost:5001/radial/1035/3`
        /radial/<start_node_id>/<int:degree>
4. `Usage - Find all the Paths: http://localhost:5001/paths/1034:1808/9`
        /paths/<start_id>:<end_id>/<int:distance>

# More Documentation will follow....
