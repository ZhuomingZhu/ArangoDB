
from arango import ArangoClient

# declare the client connection
client = ArangoClient(
protocol='http',
host='localhost',
port=8529,
username='root',
password='2222',
enable_logging=True
)

def graph_create():

    # Create a new graph
    graph = client.db('my_py_database').create_graph('drug_bank')
    subjects = graph.create_vertex_collection('subjects')
    objects = graph.create_vertex_collection('objects')
    links = graph.create_edge_definition(
        name='links',
        from_collections=['subjects'],
        to_collections=['objects']
    )

import re # package for regualar expression

# string = '... | sku: 01234 | price: 150 | sku: 99872453 | blah blah ... '
# print (re.findall(r'sku[\s:]*(\d*)', string)[0])
#
# print (re.findall(r'sku[\s:]*(\d*)', string)[1])
#
# count = 0



def graph_insert(sv,ov,linkv):
    # create the connection to insert the graph
    graph = client.db('my_py_database').graph('drug_bank')
    subjects = graph.vertex_collection('subjects')
    objects = graph.vertex_collection('objects')
    # # List existing edge definitions
    graph.edge_definitions()
    # # Retrieve an existing edge collection name
    links = graph.edge_collection('links')

    db = client.database('my_py_database')

    # Insert vertices
    # subjects.insert({'_key': 'snode03', 'subject_name': sv})
    # objects.insert({'_key': 'onode03', 'object_name': ov})
    s_exisiting_key = None
    o_exisiting_key = None
    # Execute an AQL query to get the subject key if duplicate node
    result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == "'+sv+'" return user')
    if (len(result.batch()) > 0):
        s_exisiting_key = result.batch()[0]['_key']

    result = db.aql.execute('FOR user IN objects FILTER user.object_name == "'+ov+'" return user')
    if (len(result.batch()) > 0):
        o_exisiting_key = result.batch()[0]['_key']
    # print (len(result.batch()))                   # Return the set result list length
    # print (result.statistics())                   # Return the stat info
    # print (result.statistics()['filtered'])       # Return the stat info ['filtered'] = filter value
    if s_exisiting_key is None:
        s_result = subjects.insert({'subject_name': sv})
        s_key = s_result['_key']
    else:
        s_key = s_exisiting_key
    if o_exisiting_key is None:
        o_result = objects.insert({'object_name': ov})
        o_key = o_result['_key']
    else:
        o_key = o_exisiting_key

    # Optionalto get the id, but the system can return you the id.
    # Execute an AQL query to get the database key_id
    # result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == "test_search4" return user')
    # print([subject['_key'] for subject in result])
    # objects.insert({'object_name': ov})

    # # Insert edges
    links.insert({'_from': 'subjects/'+s_key, '_to': 'objects/'+o_key, 'link_value' : linkv})
    print ('-------------- After inserted ---------------')
    print ('Subject id: ', s_key, ' Object id: ', o_key)
    print ('link by: ', linkv)

# Main program start here:
graph_create()

with open('/Users/suesalito/Desktop/ArangoDB/sampledata2.nt') as f:
    for line in f:
        string = line
        print ()
        print("====== Record no. :", count)
        count  = count +1
        # print (string)
        # print (re.findall(r'http*>', string))

        # m = re.search('<(.+?)>', string)
        try:

            print ('Subject_name :',re.findall(r'<(.+?)>', string)[0])
            print ('Object_name :',re.findall(r'<(.+?)>', string)[1])
            sv = re.findall(r'<(.+?)>', string)[0]
            ov = re.findall(r'<(.+?)>', string)[1]

            # try:
            #     print (re.findall(r'<(.+?)>', string)[2])
            # except:
            if len(re.findall(r'<(.+?)>', string)) > 2:
                print ('link_value :',re.findall(r'<(.+?)>', string)[2])
                linkv = re.findall(r'<(.+?)>', string)[2]
                graph_insert(sv,ov,linkv)
            else:
                print ('link_value :',re.findall(r'"(.+?)"', string)[0])
                linkv = re.findall(r'"(.+?)"', string)[0]
                graph_insert(sv,ov,linkv)
            # print (re.findall(r'"(.+?)"', string))
        except AttributeError:
            # AAA, ZZZ not found in the original string
            found = '' # apply your error handling










