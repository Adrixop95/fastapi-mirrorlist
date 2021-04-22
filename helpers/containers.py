# Example; crappy script
# Sample script that allows you to automatically generate a URL based on a Traefik v2 label.
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
            try:
                if value.startswith('Host'):
                    # regex stuff to filter hostname
                    host_find_brackets = re.findall(r"\(.*?\)", value)[0]
                    host_remove_quotes = re.sub("[(')]", '', host_find_brackets)[1:-1]
                    # lazy check, because I don't want to check the current host with fastapi
                    if "nginx" in host_remove_quotes:
                        container_hosts.append(host_remove_quotes)
            except TypeError:
                message = "This " + value + key + "is incorrect!"
                container_hosts.append(message)

    return container_hosts
