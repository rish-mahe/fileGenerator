import json
import yaml
import sys
import random

def fileGen(jsonObj, name, tarPort, port, commit_id):
    print commit_id
    print jsonObj
    tarPort = int(tarPort)
    port = (port)
    envVars = json.loads(jsonObj)
    jasArr = []
    for key in envVars:
        jasArr.append({'name': key.encode('ascii', 'ignore'), 'value': envVars[key].encode('ascii', 'ignore')})
    controller = {'kind': 'ReplicationController', 'spec': {'replicas': 1, 'template': {'spec': {'containers': [{'image': '10.240.255.5:5000/'+ name +':'+commit_id+'', 'name': ''+ name +'-'+commit_id+'', 'env': jasArr, 'ports': [{'containerPort': tarPort, 'name': 'http-server'}]}]}, 'metadata': {'labels': {'name': ''+ name +'', 'commit-id': ''+commit_id+''}}}, 'selector': {'name': ''+ name +'', 'commit-id': ''+commit_id+''}}, 'apiVersion': 'v1', 'metadata': {'labels': {'name': ''+ name +''}, 'name': ''+ name +'-controller-'+commit_id+''}}
    service = {'kind': 'Service', 'spec': {'type': 'ClusterIP', 'ports': [{'targetPort': tarPort, 'protocol': 'TCP', 'port': int(port)}], 'selector': {'name': name}}, 'apiVersion': 'v1', 'metadata': {'labels': {'name': name}, 'name': name}}

    with open(name+'-controller.yaml', 'w') as retFile1:
        yaml.dump(controller, retFile1, default_flow_style=False)
        retFile1.close()

    with open(name+'-service.yaml', 'w') as retFile2:
        yaml.dump(service, retFile2, default_flow_style=False)
        retFile2.close()

    with open('DockerfileGen', 'r') as retFile3:
        str = retFile3.read()
        if 'port' in str:
            str = str.replace('port', port)

    with open('Dockerfile', 'w') as retFile:
        retFile.write(str)


if __name__ == '__main__':
    if len(sys.argv)==6:
        fileGen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        fileGen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], '%032x' % random.randrange(16**32))

