from arango import ArangoClient

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='2222',
    enable_logging=True
)

# Create a new graph
# graph = client.db('my_py_database').create_graph('my_graph')
# students = graph.create_vertex_collection('students')
# courses = graph.create_vertex_collection('courses')
# takes = graph.create_edge_definition(
#     name='takes',
#     from_collections=['students'],
#     to_collections=['courses']
# )

# incase of insert
graph = client.db('my_py_database').graph('my_graph')
students = graph.vertex_collection('students')
courses = graph.vertex_collection('courses')

# takes = graph.create_edge_definition(
#     name='takes',
#     from_collections=['students'],
#     to_collections=['courses']

# # List existing edge definitions
graph.edge_definitions()
#
# # Retrieve an existing edge collection
takes = graph.edge_collection('takes')



# Insert vertices
students.insert({'_key': '001', 'full_name': 'Anna Smith'})
students.insert({'_key': '002', 'full_name': 'Jake Clark'})
students.insert({'_key': '003', 'full_name': 'Lisa Jones'})

courses.insert({'_key': 'MAT1', 'title': 'Calculus'})
courses.insert({'_key': 'STA1', 'title': 'Statistics'})
courses.insert({'_key': 'CSC1', 'title': 'Algorithms'})

# Insert edges
takes.insert({'_from': 'students/001', '_to': 'courses/MAT1'})
takes.insert({'_from': 'students/002', '_to': 'courses/STA1'})
# takes.insert({'_from': 'students/111', '_to': 'courses/CSC10111x'})
# takes.insert({'_from': 'students/222', '_to': 'courses/MAT10111x'})
# takes.insert({'_from': 'students/222', '_to': 'courses/STA10111x'})
# takes.insert({'_from': 'students/333', '_to': 'courses/CSC10111x'})

# # Traverse the graph in outbound direction, breath-first
# traversal_results = graph.traverse(
#     start_vertex='students/011',
#     strategy='bfs',
#     direction='outbound'
# )
# print(traversal_results['vertices'])