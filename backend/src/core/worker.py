from uvicorn.workers import UvicornWorker


class Worker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        # "ssl_keyfile": "./certs/server.key",
        # "ssl_certfile": "./certs/server.crt",
        "lifespan": "off",
    }
