from arango import ArangoClient

client = ArangoClient(
    protocol='http',
    host='localhost',
    port=8529,
    username='root',
    password='123456',
    enable_logging=True
)

graph = client.db('example').graph('my_graph')
students = graph.vertex_collection('students')
courses = graph.vertex_collection('courses')


graph.edge_definitions()

takes = graph.edge_collection('takes')

students.insert({'_key': '001', 'full_name': 'Anna Smith'})
students.insert({'_key': '002', 'full_name': 'Jake Clark'})
students.insert({'_key': '003', 'full_name': 'Lisa Jones'})


courses.insert({'_key': 'MAT1', 'title': 'Calculus'})
courses.insert({'_key': 'STA1', 'title': 'Statistics'})
courses.insert({'_key': 'CSC1', 'title': 'Algorithms'})

takes.insert({'_from': 'students/001', '_to': 'courses/MAT1'})
takes.insert({'_from': 'students/002', '_to': 'courses/STA1'})
