
from arango import ArangoClient
import pandas as pd
import numpy as np
import re # package for regular expression

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
    graph = client.db('my_py_database3').create_graph('drug_bank')
    subjects = graph.create_vertex_collection('subjects')
    # objects = graph.create_vertex_collection('objects')
    links = graph.create_edge_definition(
        name='links',
        from_collections=['subjects'],
        to_collections=['subjects']
    )



def get_type(type):
    check = None
    for jj in range (0,type_list.shape[0]):
        if type.find(type_list.item(jj,0)) >= 0:
            # print (type_list.item(jj,0))
            # print ("type: ",type)
            # print ("value",type_list.item(jj,0))
            vfound = type_list.item(jj,0)
            itemindex = np.where(type_list[:,0]==vfound)
            # print ("index",itemindex)
            if not itemindex :
                # print ("Not in the list")
                return 'EXT_RESOURCE'
            else:
                # print (itemindex [0][0])
                # if (type_list[itemindex [0][0],1]== 'EXT_RESOURCE'):
                #     print (type)
                # print (type_list[itemindex [0][0],1])
                return type_list[itemindex [0][0],1]
    if (check == None):
        return 'EXT_RESOURCE'

def graph_insert_withlink(sv,ov,linkv):
    # create the connection to insert the graph
    graph = client.db('my_py_database3').graph('drug_bank')
    subjects = graph.vertex_collection('subjects')
    objects = graph.vertex_collection('subjects')
    # # List existing edge definitions
    graph.edge_definitions()
    # # Retrieve an existing edge collection name
    links = graph.edge_collection('links')

    db = client.database('my_py_database3')

    # Insert vertices
    # subjects.insert({'_key': 'snode03', 'subject_name': sv})
    # objects.insert({'_key': 'onode03', 'object_name': ov})
    s_exisiting_key = None
    o_exisiting_key = None
    # Execute an AQL query to get the subject key if duplicate node
    result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == "'+sv+'" return user')
    if (len(result.batch()) > 0):
        # print ('found subject key')
        s_exisiting_key = result.batch()[0]['_key']

    result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == "'+ov+'" return user')
    if (len(result.batch()) > 0):
        # print ('found subject (Object) key')
        o_exisiting_key = result.batch()[0]['_key']
    # print (len(result.batch()))                   # Return the set result list length
    # print (result.statistics())                   # Return the stat info
    # print (result.statistics()['filtered'])       # Return the stat info ['filtered'] = filter value
    if s_exisiting_key is None:
        # stype_tmp = re.findall(r'<(.+?)>', sv)[0]
        stype = (re.findall(r'(.*)/', sv)[0]) +'/'           # Get the first part to determine type
        sreal_type = get_type(stype)
        # print ("s_real_type from inside function",sreal_type)
        s_result = subjects.insert({'subject_name': sv, 'Type':sreal_type})
        s_key = s_result['_key']
    else:
        s_key = s_exisiting_key
    if o_exisiting_key is None:
        otype = (re.findall(r'(.*)/', ov)[0]) +'/'           # Get the first part to determine type
        oreal_type = get_type(otype)
        # print ("o_real_type from inside function",oreal_type)
        o_result = objects.insert({'subject_name': ov, 'Type':oreal_type})   # as object node
        o_key = o_result['_key']
    else:
        o_key = o_exisiting_key

    # Optionalto get the id, but the system can return you the id.
    # Execute an AQL query to get the database key_id
    # result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == '
    #                         '"http://www4.wiwiss.fu-berlin.de/drugbank/resource/drugs/DB00001" return user')
    # print([subject['_key'] for subject in result])

    # # Insert edges
    links.insert({'_from': 'subjects/'+s_key, '_to': 'subjects/'+o_key, 'link_value' : linkv})
    # print ('-------------- After inserted ---------------')
    # print ('Subject id: ', s_key, ' Object id: ', o_key)
    # print ('link by: ', linkv)


def graph_insert_attribute(sv,at,atv):
    # create the connection to insert the graph
    graph = client.db('my_py_database3').graph('drug_bank')
    subjects = graph.vertex_collection('subjects')
    objects = graph.vertex_collection('subjects')
    # # List existing edge definitions
    graph.edge_definitions()
    # # Retrieve an existing edge collection name
    links = graph.edge_collection('links')

    db = client.database('my_py_database3')

    # Insert vertices
    # subjects.insert({'_key': 'snode03', 'subject_name': sv})
    # objects.insert({'_key': 'onode03', 'object_name': ov})
    s_exisiting_key = None
    o_exisiting_key = None
    # Execute an AQL query to get the subject key if duplicate node
    result = db.aql.execute('FOR user IN subjects FILTER user.subject_name == "'+sv+'" return user')
    # Result.batch is a return data structure from Arango, if it is not null, it means the record found
    if (len(result.batch()) > 0):
        # print ('found subject key')
        s_exisiting_key = result.batch()[0]['_key']

    # print (len(result.batch()))                   # Return the set result list length
    # print (result.statistics())                   # Return the stat info
    # print (result.statistics()['filtered'])       # Return the stat info ['filtered'] = filter value
    if s_exisiting_key is None:
        # stype_tmp = re.findall(r'<(.+?)>', sv)[0]
        stype = (re.findall(r'(.*)/', sv)[0]) +'/'           # Get the first part to determine type
        sreal_type = get_type(stype)
        # print ("s_real_type from outside",sreal_type)
        s_result = subjects.insert({'subject_name': sv, 'Type':sreal_type})
        s_key = s_result['_key']
    else:
        s_key = s_exisiting_key
    # print (s_key)
    # print (at)
    #
    # print (atv)
    # # Insert attribute
    result = db.aql.execute('FOR s IN subjects FILTER s._key == "' + s_key +
                            '" UPDATE s WITH { '+at+':"'+atv+'" } IN subjects')
    # print ('-------------- After inserted ---------------')
    # print ('Subject id: ', s_key, ' attribute: ',at,' value: ',atv  )
    # print (result.batch())
    # print ('link by: ', linkv)





# Main program start here:
graph_create()
count = 0

df_type = pd.read_csv('/Users/suesalito/Desktop/ArangoDB/drugbank_node_typex.csv', header=None, low_memory=False, dtype='object')

type_list = df_type.iloc[0:,0:].values
print (type_list)
print (type_list[0,0])

with open('/Users/suesalito/Desktop/ArangoDB/drugbank_dump.nt') as f:
    for line in f:
        string = line
        # print ()
        # print ("-------",count)
        if (count % 100 == 0):
            print("====== Record no. :", count)
        count  = count +1
        # print (string)
        # print (re.findall(r'http*>', string))

        # m = re.search('<(.+?)>', string)
        try:

            # print ('Subject_name :',re.findall(r'<(.+?)>', string)[0])
            # print ('Object_name :',re.findall(r'<(.+?)>', string)[1])
            sv = re.findall(r'<(.+?)>', string)[0]
            # stype_tmp = re.findall(r'<(.+?)>', string)[0]
            # stype = (re.findall(r'(.*)/', stype_tmp)[0]) +'/'           # Get the first part to determine type
            # sreal_type = get_type(stype)
            # print ("s_real_type from outside",sreal_type)

            ov = re.findall(r'<(.+?)>', string)[1]
            # otype_tmp = re.findall(r'<(.+?)>', string)[1]
            # otype = (re.findall(r'(.*)/', otype_tmp)[0]) +'/'           # Get the first part to determine type
            # oreal_type = get_type(otype)
            # print ("o_real_type from outside",oreal_type)

            # try:
            #     print (re.findall(r'<(.+?)>', string)[2])
            # except:
            if len(re.findall(r'<(.+?)>', string)) > 2:
                # print ('link_value :',re.findall(r'<(.+?)>', string)[2])
                linkv = re.findall(r'<(.+?)>', string)[2]
                graph_insert_withlink(sv,ov,linkv)
            else:
                # print ('link_value :',re.findall(r'"(.+?)"', string)[0])
                value = re.findall(r'"(.*)"', string)[0]
                # attribute_name = re.findall(r'/(.+)',ov)[0]
                # print (attribute_name)
                attribute_name = re.findall(r'\/([^/]*)$',ov)       # Get the last field from URL as attribute
                # print (attribute_name)
                attribute_name[0] = attribute_name[0].replace("-", "_")
                attribute_name[0] = attribute_name[0].replace("#", "_")
                attribute_name[0] = attribute_name[0].replace(".", "_")
                # print ("TEST",attribute_name[0])
                graph_insert_attribute(sv,attribute_name[0],value)
            # print (re.findall(r'"(.+?)"', string))
        except AttributeError:
            # AAA, ZZZ not found in the original string
            found = '' # apply your error handling







