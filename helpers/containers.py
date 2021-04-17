import re
import docker


def get_host_from_traefik():
    client_api = docker.APIClient(base_url='unix://var/run/docker.sock')
    client_env = docker.from_env()

    # Get all running containers
    running_containers = client_env.containers.list(all=True)

    container_hosts = []

    # loop trough all containers
    for i in running_containers:
        # check container labels
        container_from_id = client_api.inspect_container(i.id)['Config']['Labels']

        # if container have host definition in labels
        for key, value in container_from_id.items():
            if value.startswith('Host'):
                # regex stuff to filfer hostname
                host_find_brackets = re.findall(r"\(.*?\)", value)[0]
                host_remove_quotes = re.sub("[(')]", '', host_find_brackets)[1:-1]
                container_hosts.append(host_remove_quotes)

    return container_hosts
