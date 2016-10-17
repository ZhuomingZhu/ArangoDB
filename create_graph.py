from arango import ArangoClient

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='123456',
    enable_logging=True
)

 # Create a new graph
 graph = client.db('my_py_database').create_graph('my_graph')
 students = graph.create_vertex_collection('students')
 courses = graph.create_vertex_collection('courses')
 takes = graph.create_edge_definition(
     name='takes',
    from_collections=['students'],
    to_collections=['courses']
 )
