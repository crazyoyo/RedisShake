#!/usr/bin/env python3
# encoding: utf-8
import sys
import redis

USAGE = """
redis_full_check_command_generator is a helper generate redis_full_check command in cluster mode.

Usage:
   $ python3 redis_full_check_command_generator.py <source_endpoint> <target_endpoint>
"""

COMMAND_TEMPLATE = 'bin/redis-full-check -s "{}" -t "{}" --comparetimes=1 --sourcedbtype=1 --targetdbtype=1'

def main():
    if len(sys.argv) != 2:
        print(USAGE)
        exit(1)

    # parse args
    sourcehost, sourceport = sys.argv[1].split(":")
    targethost, targetport  = sys.argv[2].split(":")

    print(
        f"source: {sourcehost}:{sourceport}, target: {targethost}:{targetport}"
    )
    source_cluster = redis.RedisCluster(
        host=sourcehost, port=sourceport
    )
    print("source cluster nodes:", source_cluster.cluster_nodes())
    source_masters = ""
    for s in source_cluster.get_primaries():
        source_masters += s.name + ";"

    target_cluster = redis.RedisCluster(
        host=targethost, port=targetport
    )
    print("target cluster nodes:", target_cluster.cluster_nodes())
    target_masters = ""
    for t in target_cluster.get_primaries():
        target_masters += t.name + ";"

    print("the redis-full-check command is:", COMMAND_TEMPLATE.format())


if __name__ == "__main__":
    main()
