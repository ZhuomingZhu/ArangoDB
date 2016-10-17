
#     lines = f.readlines()
#     print (lines)
# words = lines.split(".\n")
#
# print (words)

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""



s = 'asdf=5;iwantthis123jasd'


# with open('/Users/suesalito/Desktop/ArangoDB/sampledata.nt') as f:
#     for line in f:
            # print (line)
            # print (find_between_r( line, "<", ">" ))
            # result = re.search('<(.*)> ', line)
            # print (result.groups())
            # print (line.split(' '))

#
# >>> import re
# >>> string = '... | sku: 01234 | price: 150 | sku: 99872453 | blah blah ... '
# >>> re.findall(r'sku[\s:]*(\d*)', string)[0]
# '01234'
# >>> re.findall(r'sku[\s:]*(\d*)', string)[1]
# '99872453'

import re # package for regualar expression

string = '... | sku: 01234 | price: 150 | sku: 99872453 | blah blah ... '
print (re.findall(r'sku[\s:]*(\d*)', string)[0])

print (re.findall(r'sku[\s:]*(\d*)', string)[1])

count = 0

with open('/Users/suesalito/Desktop/ArangoDB/sampledata2.nt') as f:
    for line in f:
        string = line
        print("====== Line no. :", count)
        count  = count +1
        # print (string)
        # print (re.findall(r'http*>', string))

        # m = re.search('<(.+?)>', string)
        try:
            # found = re.search('<(.+?)>', string).group(1)
            # print (found)
            # # found = re.search('<(.+?)>', string).group(2)
            # # print (found)
            # found = re.match('<(.+?)>', string).group(1)
            # print (found)
            # found = re.match('<(.+?)>', string).group(2)
            # print (found)
            # found = re.match('<(.+?)>', string).group(0)
            # print (found)

            print (re.findall(r'<(.+?)>', string)[0])
            print (re.findall(r'<(.+?)>', string)[1])
            # try:
            #     print (re.findall(r'<(.+?)>', string)[2])
            # except:
            if len(re.findall(r'<(.+?)>', string)) > 2:
                print (re.findall(r'<(.+?)>', string)[2])
            else:
                print (re.findall(r'"(.+?)"', string)[0])
            # print (re.findall(r'"(.+?)"', string))
        except AttributeError:
            # AAA, ZZZ not found in the original string
            found = '' # apply your error handling





