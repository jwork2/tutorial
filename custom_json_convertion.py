"""
# test custom json convertion
"""


sample = {"hello":"world","hi":"clo","num":"45646","apps":"[4,'nuke','houdini','blender','katana']","name":"user"}

json = str(sample)

print(json)
print()

data = json.split('\':')
jk = []
for x in range(len(data)-1):
    jk.append(data[x].split('\':')[0].rsplit('\'',1)[1].strip())
    if x+1 == range(len(data)-1):
        jk[x] = jk[x].strip('\'')

print(jk)

jv = []
for x in range(len(data)-1):
    y = 1
    if x+1 == len(data)-1:
        y=0
    jv.append(json.split(jk[x]+'\':')[1].split(', \''+jk[x+y])[0].strip())
    if not y:
        jv[-1] = jv[-1].strip('}')
        for x in range(len(jv)):
            jv[x] = jv[x].strip('\'')

print()
print(jv)

result = {}
for x in range(len(jk)):
    result[jk[x]]=jv[x]

print()
print(result)
