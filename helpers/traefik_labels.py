import re
import docker


def add_to_list(lst, string):
    string += '{0}'
    lst = [string.format(i) for i in lst]
    return lst


def get_host_from_traefik():
    client_api = docker.APIClient(base_url='unix://var/run/docker.sock')
    client_env = docker.from_env()

    running_containers = client_env.containers.list(all=True)

    container_hosts = []

    # senselessly high computational complexity to be rewritten
    for i in running_containers:
        container_from_id = client_api.inspect_container(i.id)['Config']['Labels']
        for key, value in container_from_id.items():
            if key.startswith('traefik.http.routers') and re.search("Host", value):
                if value.count('`') > 4:
                    unified_value = value.replace(" ", "")
                    base_host = unified_value.partition("Host(`")[2].partition("`)")[0]

                    prefixes = re.sub(r"[(|)|`|&|\s+]", r"",
                                      unified_value.partition("&&PathPrefix(`")[2].partition('`)')[0]).split(",")

                    container_hosts.extend(add_to_list(prefixes, base_host))
                else:
                    regex_cleanup = re.sub(r"[(|)|`|&|\s+]", r"", value)
                    string_cleanup = regex_cleanup.replace("Host", "").replace("PathPrefix", "").strip()
                    container_hosts.append(string_cleanup)

    return container_hosts
