# Docker Networking
- User-defined bridge networks: best when multiple containers on same docker host
- Host networks: uses docker host's actual network stack
- Overlay networks: used when containers running on different hosts need to communicate

## [Networking with Standalone Containers](https://docs.docker.com/network/network-tutorial-standalone/)
- Docker offers default bridge network but not ideal for prod
- Better off using a user defined bridge network

### Using Default Bridge Network
- `docker network ls` shows: `bridge`, `host` and `none` for using that type of network respectively
- Run to `ash` (docker shell) alpine instances in in detatched (`-dit`) mode: `docker run -dit --name alpine1 alpine ash`
    - No network specified so uses default bridge
    - `docker container ls`
- Inspect bridge network status `docker network inspect bridge`: Shows:
    - Gateway from docker host --> bridge network
    - Containers using this network and their IPs
- Attach to docker container `docker attach alpine1`
    - `ip addr show` to see the `eth` connection to the bridge network
    - `ping <other_ip>` should hit the other docker container
    - `ping alpine2` fails though using default brdige network

### Using user-defined bridge network
- Create custom network `docker network create --driver bridge alpine-net`
- `docker network ls` shows it, `docker network inspect alpine-net`
    - Gateway is eg `172.18.0.1` as opposed to default bridge net's gateway which is `172.17.0.1`
- Create containers `docker run -dit --name alpine[1,2,4] --network alpine-net alpine ash`
- Create container `docker run -dit --name alpine3 alpine ash`
    - This connects to default bridge network
- Connect 4 to the default bridge network aswell with `docker network connect bridge alpine4`
- (this was just to create a topology)
- Containers can resolve container names --> IP addresses 
    - `docker container attach alpine1`
    - `ping -c 2 alpine{1,2,4}`
    - `ping -c 2 alpine3` - fails as alpine 3 isn't connected to alpine-net and alpine 1 is not connected to bridge
        - Can't hit it directly with IP either!
- Attaching into alpine4 (connected to both networks)
    - `ping alpine1` succeeds
    - `ping alpine3` fails but `ping <ip_of_alpine3>` works!
    - Should be able to ping internet on any of the containers

## [Using Bridge Networks](https://docs.docker.com/network/bridge/)
