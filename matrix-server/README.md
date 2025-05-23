```
docker run -it --rm \
    -v $(pwd)/synapse/data:/data \
    -e SYNAPSE_SERVER_NAME=matrix.local \
    -e SYNAPSE_REPORT_STATS=no \
    matrixdotorg/synapse:latest generate

```

```
docker exec -it synapse register_new_matrix_user -c /data/homeserver.yaml http://localhost:8008 -a
```

```
mkdir -p synapse/data
mkdir -p element
```