import os

os.environ["BEARTYPE_DISABLE"] = "1"

import json
import time
import gc
import tracemalloc
from pathlib import Path
from typing import Dict, List, Any, Tuple, Union
from datetime import datetime
import argparse

from pyecs import ECSWorld, Entity, StatusCodes, Query
from dataclasses import dataclass


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Velocity:
    dx: float = 0.0
    dy: float = 0.0
    dz: float = 0.0


@dataclass
class Health:
    current: int = 100
    max: int = 100


@dataclass
class Name:
    value: str = "Entity"


class BenchmarkRunner:
    def __init__(self, iterations: int = 10, warmup: int = 2):
        self.iterations = iterations
        self.warmup = warmup
        self.results: Dict[str, Any] = {}

    def measure_time(self, func, *args, **kwargs) -> List[float]:
        times = []

        for _ in range(self.warmup):
            func(*args, **kwargs)

        for _ in range(self.iterations):
            gc.collect()
            gc.disable()

            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()

            gc.enable()
            times.append(end - start)

        return times

    def benchmark_entity_creation(self, entity_counts: List[int]) -> Dict[str, List[float]]:
        print("\n=== Entity Creation Benchmarks ===")
        results = {}

        for count in entity_counts:
            print(f"Creating {count} entities...")

            def create_entities():
                world = ECSWorld()
                entities = []

                for i in range(count):
                    entity = world.create_entity()
                    if entity != StatusCodes.FAILURE:
                        world.add_component(entity, Position(i, i * 2, i * 3))
                        world.add_component(entity, Velocity(i * 0.1, i * 0.2, i * 0.3))
                        if i % 2 == 0:
                            world.add_component(entity, Health(100 - i % 50, 100))
                        if i % 3 == 0:
                            world.add_component(entity, Name(f"Entity_{i}"))
                        entities.append(entity)

                return world, entities

            times = self.measure_time(create_entities)
            results[str(count)] = times
            print(f"  Average: {sum(times) / len(times):.6f}s")

        return results

    def benchmark_query_performance(
        self, entity_counts: List[int]
    ) -> Dict[str, Dict[str, List[float]]]:
        print("\n=== Query Performance Benchmarks ===")
        results = {"single_component": {}, "two_components": {}, "three_components": {}}

        for count in entity_counts:
            print(f"Testing queries on {count} entities...")

            world = ECSWorld()
            for i in range(count):
                entity = world.create_entity()
                if entity != StatusCodes.FAILURE:
                    world.add_component(entity, Position(i, i * 2, i * 3))
                    if i % 2 == 0:
                        world.add_component(entity, Velocity(i * 0.1, i * 0.2, i * 0.3))
                    if i % 3 == 0:
                        world.add_component(entity, Health(100 - i % 50, 100))
                    if i % 4 == 0:
                        world.add_component(entity, Name(f"Entity_{i}"))

            def query_single():
                query = Query().with_components(Position)
                entities = query.execute(world.component_storage)
                total = 0
                for entity in entities:
                    pos = world.get_component(entity, Position)
                    if isinstance(pos, Position):
                        total += pos.x + pos.y + pos.z
                return total

            def query_two():
                query = Query().with_components(Position, Velocity)
                entities = query.execute(world.component_storage)
                total = 0
                for entity in entities:
                    pos = world.get_component(entity, Position)
                    vel = world.get_component(entity, Velocity)
                    if isinstance(pos, Position) and isinstance(vel, Velocity):
                        total += pos.x * vel.dx
                return total

            def query_three():
                query = Query().with_components(Position, Velocity, Health)
                entities = query.execute(world.component_storage)
                total = 0
                for entity in entities:
                    pos = world.get_component(entity, Position)
                    vel = world.get_component(entity, Velocity)
                    health = world.get_component(entity, Health)
                    if (
                        isinstance(pos, Position)
                        and isinstance(vel, Velocity)
                        and isinstance(health, Health)
                    ):
                        total += (pos.x * vel.dx) * (health.current / health.max)
                return total

            results["single_component"][str(count)] = self.measure_time(query_single)
            results["two_components"][str(count)] = self.measure_time(query_two)
            results["three_components"][str(count)] = self.measure_time(query_three)

            print(
                f"  Single component: {sum(results['single_component'][str(count)]) / self.iterations:.6f}s"
            )
            print(
                f"  Two components: {sum(results['two_components'][str(count)]) / self.iterations:.6f}s"
            )
            print(
                f"  Three components: {sum(results['three_components'][str(count)]) / self.iterations:.6f}s"
            )

        return results

    def benchmark_component_operations(
        self, operation_counts: List[int]
    ) -> Dict[str, Dict[str, List[float]]]:
        print("\n=== Component Operation Benchmarks ===")
        results = {"add": {}, "remove": {}, "get": {}}

        for count in operation_counts:
            print(f"Testing {count} operations...")

            world = ECSWorld()
            entities = []
            for i in range(1000):
                entity = world.create_entity()
                if entity != StatusCodes.FAILURE:
                    world.add_component(entity, Position(i, i, i))
                    entities.append(entity)

            def add_components():
                for i in range(count):
                    entity = entities[i % len(entities)]
                    world.add_component(entity, Velocity(i, i, i))

            def remove_components():
                for entity in entities:
                    world.add_component(entity, Health())
                for i in range(count):
                    entity = entities[i % len(entities)]
                    world.remove_component(entity, Health)

            def get_components():
                total = 0
                for i in range(count):
                    entity = entities[i % len(entities)]
                    pos = world.get_component(entity, Position)
                    if isinstance(pos, Position):
                        total += pos.x
                return total

            results["add"][str(count)] = self.measure_time(add_components)
            results["remove"][str(count)] = self.measure_time(remove_components)
            results["get"][str(count)] = self.measure_time(get_components)

            print(f"  Add: {sum(results['add'][str(count)]) / self.iterations:.6f}s")
            print(f"  Remove: {sum(results['remove'][str(count)]) / self.iterations:.6f}s")
            print(f"  Get: {sum(results['get'][str(count)]) / self.iterations:.6f}s")

        return results

    def benchmark_memory_usage(self, entity_counts: List[int]) -> Dict[str, List[float]]:
        print("\n=== Memory Usage Benchmarks ===")
        results = {}

        for count in entity_counts:
            print(f"Measuring memory for {count} entities...")
            memory_measurements = []

            for _ in range(5):
                gc.collect()

                tracemalloc.start()

                world = ECSWorld()
                entities = []
                for i in range(count):
                    entity = world.create_entity()
                    if entity != StatusCodes.FAILURE:
                        world.add_component(entity, Position(i, i * 2, i * 3))
                        world.add_component(entity, Velocity(i * 0.1, i * 0.2, i * 0.3))
                        if i % 2 == 0:
                            world.add_component(entity, Health(100 - i % 50, 100))
                        if i % 3 == 0:
                            world.add_component(entity, Name(f"Entity_{i}"))
                        entities.append(entity)

                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                memory_measurements.append(float(current))

            results[str(count)] = memory_measurements
            avg_memory = sum(memory_measurements) / len(memory_measurements)
            print(f"  Average: {avg_memory / (1024 * 1024):.2f} MB")

        return results

    def run_all_benchmarks(
        self, entity_counts: List[int] = None, operation_counts: List[int] = None
    ) -> Dict[str, Any]:
        if entity_counts is None:
            entity_counts = [100, 1000, 10000, 100000]
        if operation_counts is None:
            operation_counts = [100, 1000, 10000]

        print(f"Starting PyECS Benchmarks")
        print(f"Iterations: {self.iterations}, Warmup: {self.warmup}")
        print(f"Entity counts: {entity_counts}")
        print(f"Operation counts: {operation_counts}")

        start_time = time.time()

        self.results = {
            "entity_creation": self.benchmark_entity_creation(entity_counts),
            "query_performance": self.benchmark_query_performance(entity_counts),
            "component_operations": self.benchmark_component_operations(operation_counts),
            "memory_usage": self.benchmark_memory_usage(entity_counts),
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "system": "PyECS",
                "version": "0.1.0",
                "iterations": self.iterations,
                "warmup": self.warmup,
                "entity_counts": entity_counts,
                "operation_counts": operation_counts,
                "total_time": 0,
            },
        }

        total_time = time.time() - start_time
        self.results["metadata"]["total_time"] = total_time

        print(f"\nBenchmarks completed in {total_time:.2f} seconds")

        return self.results

    def save_results(self, filepath: Union[str, Path]) -> None:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"Results saved to: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Run benchmarks on PyECS")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        help="Output file for benchmark results",
    )
    parser.add_argument(
        "--iterations", "-i", type=int, default=10, help="Number of iterations per benchmark"
    )
    parser.add_argument("--warmup", "-w", type=int, default=2, help="Number of warmup iterations")
    parser.add_argument(
        "--quick", "-q", action="store_true", help="Run quick benchmarks with smaller entity counts"
    )
    parser.add_argument(
        "--ultra-quick",
        "-uq",
        action="store_true",
        help="Run ultra-quick benchmarks (minimal iterations, smallest counts)",
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Automatically generate visualizations after benchmarking",
    )

    args = parser.parse_args()

    if args.ultra_quick:
        entity_counts = [100, 500, 1000]
        operation_counts = [50, 100]
        args.iterations = min(args.iterations, 3)
        args.warmup = min(args.warmup, 1)
    elif args.quick:
        entity_counts = [100, 1000, 5000]
        operation_counts = [100, 500]
    else:
        entity_counts = [100, 1000, 10000, 50000]
        operation_counts = [100, 1000, 5000]

    runner = BenchmarkRunner(iterations=args.iterations, warmup=args.warmup)
    results = runner.run_all_benchmarks(entity_counts, operation_counts)
    runner.save_results(args.output)

    if args.visualize:
        print("\nGenerating visualizations...")
        import subprocess

        subprocess.run(["python", "benchmark_visualizer.py", "-i", args.output])


if __name__ == "__main__":
    main()
