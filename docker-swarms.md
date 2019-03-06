# Swarms
- Orchestration among collection of docker hosts
- Docker hosts can act as managers, workers or both


## Nodes
- Instance of docker engine participating in swarms
- Submit service definition to manager nodes
    - They then dispatch unots of work (tasks) to workers
- Manager nodes elect a single leader to orchestrate
- Manager nodes can optionally also be worker nodes

## Services
- Definition of tasks to execute on workers / managers
- Main mechanism for interacting with the swam
- Services can be _replicated_ across multiple nodes
- Can also be _global_ (run on every node)

## Task
- Contains a docker container and the commands to run inside the container
- Atomic scheduling unor of swarm
- Managers assign tasks to nodes
    - Once task is assigned to a node, it cannot be moved
    - Either runs or fails

## Load Balancing
- Ingress load balancing
- All services have a `PublishedPort` which is configurable (or automatic)
    - Can access externally by using `PublishedPort` on any node 
    - All nodes route ingress connections to a relevant running task instance

## Initialize Swarm
- Choose a manager with a fixed IP and initialize the swarm `docker swarm init --advertise-addr <ip>`
- See it with `docker node ls`
- On worker machine
    - Run the command output from swarm init or `docker swarm join-token worker`
    - `docker node ls` should show added nodes (only works on manager node)

## Deploy Service to the Swarm
- On manager node
    - `docker service create --replicas 1 --name myservicename alpine ping docker.com`
    - See services running on this swarm `docker service ls`
- Inspect service on manager with:
    - `docker service inspect --pretty <service_id or service_name>`
- See which nodes are running service
    - `docker service ps <service_id or service_name>`

## Scale the service
- Scale number of containers in the service (containers running in a service are called _tasks_)
- On manager node
    - `docker service scale <service-id or service-name>=<desired_num_tasks>`
    - `docker service ps <service_name>` shows new tasks

## Delete service running on swarm
- On manager
    - `docker service rm <service_name>`

## Updating images of running Services
- Create task as before `docker service create ...`
    - By default this is one at a time with `--update-delay` in between them
    - Can set parallelism with `--update-parallelism`
- Update with:
    - `docker service update --image <image-name>:tag <service_name>`
- This stops, updates and restarts the tasks
    - If any fail, the update pauses
- To restart paused update (if one fails)
    - `docker service update <service_name>`
- Watch update with: `docker service ps <service_name>`

## Drain a node
- Typically nodes sit in `ACTIVE` state and can receive tasks
- Nodes can be drained
    - Prevents nodes from receiving new tasks 
    - Manager will start replica tasks on nodes which are `ACTIVE`
    - This **only** affects tasks scheduled by swarm
        - Does not impact `docker run ..` or `docker-compose up` containers
- On manager:
    - `docker node update --availability drain <node_id>`
    - ...maintenance...
    - `docker node update --availability active <node_name>`

## Deploy a stack to a swarm
- Deploying stacks in form of compose file
    - **Only supports compose v3.0+**
- Even if engine is in swarm mode, `docker-compose up` still uses single node and starts all containers on local host machine
- To deploy the stack to the swarm:
    - `docker stack deploy --compose-file docker-compose.yml <name>`
    - Bring it down with `docker stack rm <name>`

# Swarm Networking
Not entirely clear on this yet

## Swarm Routing Mesh
- Docker swarms use published ports to provide external access
- All nodes participate in _ingress routing mesh_
- This allows any node in the swarm to accept connections on published ports for **any service** running in the swarm, even if no tasks running on the node
- Need to open ports
    - `7946 TCP/UDP` for container network discovery
    - `4789 UDP` for container ingress network
    - And the service level port for external connections obviously
- skipping ...

## Overlay Networks
- Creates a distributed network among multiple docker daemon hosts
- Docker handles routing packets to appropriate docker hosts
- Docker swarms create two networks:
    - `ingress`: an overlay network (if no user specified overlay)
    - `docker_gwbridge`: connects individual Docker dameon to other daemons in the swarm
        - Actually connects overlay networks (e.g. ingress) to docker daemon's physical network 
- Swarm services on same overlay expose all ports to each other
    - To expose port external to overlay net use `--publish` for `docker service create|update`
        - e.g. `docker service create ... -p published=8080, target=80, protocol=TCP|UDP`
            - Maps the service's port 80 --> port 8080 on the routing mesh
- Attachable
    - `--attachable` networks allow standalone containers (non-swarm) running on different docker hosts to communicate with each other
    - Publish ports using above publish notation
- Creating user defined overlay net
    - `docker network create -d overlay <network_name>` (only  need to do this on manager)
- Create service using that network 
```shell
docker service create \
  --name my-nginx \
  --publish target=80,published=8080 \
  --replicas=5 \
  --network nginx-net \
  nginx
```
- Can now reach this node using `actual_ip_of_host:8080`
- This used the default `mode` for the `--publish` flag
    - This means requests to any node will be routed to some task by docker
- Alternatively can use:
    - `--publish... mode=host` and `--global`
        - This will run the service on every connected node
        - However this means only one service can run per node (I think) since only one service can bind to a single port
- `docker network inspect <overlay_net_name>`
    - Shows containers connected to this network (can be both swarm and standaloneS)
    - Also shows actual IPs under `peers` which is interesting
- Can move service to different networks: `docker service update --network-add new_net --network-rm oldnet <service_name>`

### Hooking up to alpine instances (standalone) on seperate Daemons
- Need TCP:2377, TCP/UDP:7946 and UDP:4789 to be open
- Create network on one of the hosts
    - `docker network create --driver=overlay --attachable test-net`
- Start alpine on host 1
    - `docker run -it --name alpine1 --network test-net alpine`
- Network obviously not yet available on node2
- Start detatched container on node 2
    - `docker run -dit --name alpine2 --network test-net alpine`
    - **This uses DNS discovery to find / create test-net!**
        - This only works if `--name`s are unique
        - Verify **ids** of networks are the same
- Can now ping alpine 2 from alpine 1
- Stop container on host 2 will remove test-net from host 2
- Can limit which nodes get what with boolean expressions
    - `--constrain node.hostname == nodea`