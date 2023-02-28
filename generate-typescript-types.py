#!/usr/bin/env python

import os
import shutil
import socket
import time
from contextlib import closing, contextmanager
from subprocess import Popen, run

DEST = os.path.join(os.path.dirname(__file__), "frontend/src/api/generated.ts")


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def find_cmd(cmd):
    path = shutil.which(cmd)
    if path is None:
        raise RuntimeError(f"Can't find the executable {cmd}")
    return path


@contextmanager
def running(cmd):
    proc = Popen(cmd)
    try:
        yield proc
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def main():
    port = find_free_port()
    fmn_cmd = find_cmd("fmn")
    npx_cmd = find_cmd("npx")
    os.environ["DATABASE__SQLALCHEMY__URL"] = "sqlite:///"
    print("Running API")
    with running([fmn_cmd, "api", "serve", "--port", str(port)]):
        time.sleep(2)
        print("Building Typescript types")
        cmd = [
            npx_cmd,
            "--yes",
            "openapi-typescript",
            f"http://127.0.0.1:{port}/openapi.json",
            "--output",
            DEST,
        ]
        print(" ".join(cmd))
        run(cmd)
        print("Shutting down API")


if __name__ == "__main__":
    main()
