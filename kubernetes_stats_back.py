from kubernetes import client, config


def ClusterRead(cluster):
    config.load_kube_config(context=cluster)
    v1 = client.AppsV1Api()
    ret = v1.list_deployment_for_all_namespaces(watch=False)
    result = []
    for i in ret.items:
        namespace = str(i.metadata.namespace)
        try:
            product_label = str(i.metadata.labels['product'])
        except:
            product_label = "No data"

        deployment_name = str(i.metadata.name)
        available_replicas = str(i.status.available_replicas)
        for cont in i.spec.template.spec.containers:
            if available_replicas != 'None':
                container_name = cont.name
                try:
                    container_request_memory = str(cont.resources.requests['memory'])
                except:
                    container_request_memory = "No data"
                try:
                    container_request_cpu = str(cont.resources.requests['cpu'])
                except:
                    container_request_cpu = "No data"
                try:
                    container_limit_memory = str(cont.resources.limits['memory'])
                except:
                    container_limit_memory = "No data"
                try:
                    container_limit_cpu = str(cont.resources.limits['cpu'])
                except:
                    container_limit_cpu = "No data"
                result.append(
                    cluster + ';' + namespace + ';' + product_label + ';' + deployment_name + ';' + available_replicas + ';' + container_name + ';' + container_request_memory + ";" + container_request_cpu + ";" + container_limit_memory + ";" + container_limit_cpu)
    return (result)


with open('tab.csv', 'a') as f:
    head = "cluster;namespace;product_label;deployment_name;available_replicas;container_name;container_request_memory;container_request_cpu;container_limit_memory;container_limit_cpu"
    print(head, file=f)
    contexts = config.list_kube_config_contexts()
    for i in contexts[0]:
        cluster = i['context']['cluster']
        output = ClusterRead(cluster)
        for i in output:
            print(i, file=f)
