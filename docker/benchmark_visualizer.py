import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.figure import Figure
from matplotlib.ticker import EngFormatter, ScalarFormatter, FuncFormatter
import seaborn as sns
from datetime import datetime


class BenchmarkVisualizer:
    def __init__(self, style: str = "seaborn-v0_8-darkgrid"):
        plt.style.use(style)
        self.colors = sns.color_palette("husl", 8)

    @staticmethod
    def format_time(seconds: float) -> str:
        if seconds < 1e-6:
            return f"{seconds * 1e9:.1f}ns"
        elif seconds < 1e-3:
            return f"{seconds * 1e6:.1f}μs"
        elif seconds < 1:
            return f"{seconds * 1e3:.1f}ms"
        else:
            return f"{seconds:.2f}s"

    @staticmethod
    def time_formatter(x, pos):
        if x < 1e-6:
            return f"{x * 1e9:.0f}ns"
        elif x < 1e-3:
            return f"{x * 1e6:.0f}μs"
        elif x < 1:
            return f"{x * 1e3:.0f}ms"
        else:
            return f"{x:.1f}s"

    def setup_time_axis(self, ax, axis="y"):
        formatter = FuncFormatter(self.time_formatter)
        if axis == "y":
            ax.yaxis.set_major_formatter(formatter)
        else:
            ax.xaxis.set_major_formatter(formatter)

        ax.grid(True, which="major", alpha=0.5)
        ax.grid(True, which="minor", alpha=0.2)
        ax.minorticks_on()

    def load_benchmark_data(self, filepath: Union[str, Path]) -> Dict[str, Any]:
        with open(filepath, "r") as f:
            return json.load(f)

    def plot_entity_creation(
        self, data: Dict[str, List[float]], title: str = "Entity Creation Performance"
    ) -> Figure:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        entity_counts = sorted([int(k) for k in data.keys()])
        times = [np.mean(data[str(count)]) for count in entity_counts]
        stds = [np.std(data[str(count)]) for count in entity_counts]

        line = ax1.errorbar(
            entity_counts,
            times,
            yerr=stds,
            marker="o",
            capsize=5,
            capthick=2,
            color=self.colors[0],
            linewidth=2,
            markersize=8,
        )

        for i, (x, y) in enumerate(zip(entity_counts, times)):
            ax1.annotate(
                self.format_time(y),
                xy=(x, y),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

        ax1.set_xlabel("Number of Entities", fontsize=12)
        ax1.set_ylabel("Time", fontsize=12)
        ax1.set_title(f"{title} - Time Scaling", fontsize=14, fontweight="bold")
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        self.setup_time_axis(ax1, "y")

        entities_per_sec = [count / time for count, time in zip(entity_counts, times)]
        ax2.plot(
            entity_counts,
            entities_per_sec,
            marker="s",
            color=self.colors[1],
            linewidth=2,
            markersize=8,
        )

        for i, (x, y) in enumerate(zip(entity_counts, entities_per_sec)):
            ax2.annotate(
                f"{y:.0f}/s",
                xy=(x, y),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

        ax2.set_xlabel("Number of Entities", fontsize=12)
        ax2.set_ylabel("Entities/Second", fontsize=12)
        ax2.set_title(f"{title} - Throughput", fontsize=14, fontweight="bold")
        ax2.set_xscale("log")
        ax2.yaxis.set_major_formatter(EngFormatter(unit=""))
        ax2.grid(True, which="major", alpha=0.5)
        ax2.grid(True, which="minor", alpha=0.2)
        ax2.minorticks_on()

        plt.tight_layout()
        return fig

    def plot_query_performance(
        self, data: Dict[str, Dict[str, List[float]]], title: str = "Query Performance"
    ) -> Figure:
        fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(2, 2, figure=fig)

        query_types = list(data.keys())

        ax1 = fig.add_subplot(gs[0, :])
        positions = np.arange(len(query_types))

        for i, query_type in enumerate(query_types):
            times = []
            labels = []
            for entity_count, measurements in data[query_type].items():
                times.append(np.mean(measurements))
                labels.append(f"{entity_count} entities")

            x = positions[i] + np.linspace(-0.3, 0.3, len(times))
            ax1.bar(x, times, width=0.6 / len(times), label=labels if i == 0 else "", alpha=0.8)

        ax1.set_xticks(positions)
        ax1.set_xticklabels(query_types, rotation=45, ha="right")
        ax1.set_ylabel("Average Query Time", fontsize=12)
        ax1.set_title(f"{title} - Query Time Comparison", fontsize=14, fontweight="bold")
        ax1.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax1.set_yscale("log")
        self.setup_time_axis(ax1, "y")

        ax2 = fig.add_subplot(gs[1, 0])
        for i, query_type in enumerate(query_types):
            entity_counts = sorted([int(k) for k in data[query_type].keys()])
            times = [np.mean(data[query_type][str(count)]) for count in entity_counts]
            ax2.plot(
                entity_counts,
                times,
                marker="o",
                label=query_type,
                color=self.colors[i],
                linewidth=2,
            )

        ax2.set_xlabel("Number of Entities", fontsize=12)
        ax2.set_ylabel("Query Time", fontsize=12)
        ax2.set_title("Query Time Scaling", fontsize=14, fontweight="bold")
        ax2.set_xscale("log")
        ax2.set_yscale("log")
        ax2.legend()
        self.setup_time_axis(ax2, "y")

        ax3 = fig.add_subplot(gs[1, 1])
        for i, query_type in enumerate(query_types):
            entity_counts = sorted([int(k) for k in data[query_type].keys()])
            times = [np.mean(data[query_type][str(count)]) for count in entity_counts]
            throughput = [count / time for count, time in zip(entity_counts, times)]
            ax3.plot(
                entity_counts,
                throughput,
                marker="s",
                label=query_type,
                color=self.colors[i],
                linewidth=2,
            )

        ax3.set_xlabel("Number of Entities", fontsize=12)
        ax3.set_ylabel("Entities Processed/Second", fontsize=12)
        ax3.set_title("Query Throughput", fontsize=14, fontweight="bold")
        ax3.set_xscale("log")
        ax3.yaxis.set_major_formatter(EngFormatter(unit=""))
        ax3.legend()
        ax3.grid(True, which="major", alpha=0.5)
        ax3.grid(True, which="minor", alpha=0.2)
        ax3.minorticks_on()

        plt.tight_layout()
        return fig

    def plot_component_operations(
        self, data: Dict[str, Dict[str, List[float]]], title: str = "Component Operations"
    ) -> Figure:
        operations = list(data.keys())
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()

        for i, (op, ax) in enumerate(zip(operations[:3], axes[:3])):
            if op in data:
                op_data = []
                labels = []
                for entity_count, measurements in sorted(data[op].items()):
                    op_data.append(measurements)
                    labels.append(f"{entity_count}")

                bp = ax.boxplot(op_data, labels=labels, patch_artist=True)
                for patch in bp["boxes"]:
                    patch.set_facecolor(self.colors[i])

                ax.set_xlabel("Number of Entities", fontsize=11)
                ax.set_ylabel("Time", fontsize=11)
                ax.set_title(
                    f"{op.capitalize()} Component - Time Distribution",
                    fontsize=12,
                    fontweight="bold",
                )
                ax.set_yscale("log")
                ax.tick_params(axis="x", rotation=45)
                self.setup_time_axis(ax, "y")

        ax4 = axes[3]
        for i, op in enumerate(operations):
            if op in data:
                entity_counts = sorted([int(k) for k in data[op].keys()])
                avg_times = [np.mean(data[op][str(count)]) for count in entity_counts]
                ax4.plot(
                    entity_counts,
                    avg_times,
                    marker="o",
                    label=op.capitalize(),
                    color=self.colors[i],
                    linewidth=2,
                )

        ax4.set_xlabel("Number of Entities", fontsize=11)
        ax4.set_ylabel("Average Time", fontsize=11)
        ax4.set_title("Component Operations Comparison", fontsize=12, fontweight="bold")
        ax4.set_xscale("log")
        ax4.set_yscale("log")
        ax4.legend()
        self.setup_time_axis(ax4, "y")

        plt.tight_layout()
        return fig

    def plot_memory_usage(
        self, data: Dict[str, List[float]], title: str = "Memory Usage"
    ) -> Figure:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        entity_counts = sorted([int(k) for k in data.keys()])
        memory_mb = [np.mean(data[str(count)]) / (1024 * 1024) for count in entity_counts]
        memory_std = [np.std(data[str(count)]) / (1024 * 1024) for count in entity_counts]

        ax1.errorbar(
            entity_counts,
            memory_mb,
            yerr=memory_std,
            marker="o",
            capsize=5,
            color=self.colors[2],
            linewidth=2,
            markersize=8,
        )

        for i, (x, y) in enumerate(zip(entity_counts, memory_mb)):
            ax1.annotate(
                f"{y:.2f} MB",
                xy=(x, y),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

        ax1.set_xlabel("Number of Entities", fontsize=12)
        ax1.set_ylabel("Memory Usage (MB)", fontsize=12)
        ax1.set_title(f"{title} - Total Memory", fontsize=14, fontweight="bold")
        ax1.set_xscale("log")
        ax1.grid(True, which="major", alpha=0.5)
        ax1.grid(True, which="minor", alpha=0.2)
        ax1.minorticks_on()

        memory_per_entity_kb = [
            (mem * 1024) / count for mem, count in zip(memory_mb, entity_counts)
        ]
        ax2.plot(
            entity_counts,
            memory_per_entity_kb,
            marker="s",
            color=self.colors[3],
            linewidth=2,
            markersize=8,
        )

        for i, (x, y) in enumerate(zip(entity_counts, memory_per_entity_kb)):
            ax2.annotate(
                f"{y:.1f} KB",
                xy=(x, y),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
            )

        ax2.set_xlabel("Number of Entities", fontsize=12)
        ax2.set_ylabel("Memory per Entity (KB)", fontsize=12)
        ax2.set_title(f"{title} - Memory Efficiency", fontsize=14, fontweight="bold")
        ax2.set_xscale("log")
        ax2.grid(True, which="major", alpha=0.5)
        ax2.grid(True, which="minor", alpha=0.2)
        ax2.minorticks_on()

        plt.tight_layout()
        return fig

    def plot_comparison(
        self, datasets: Dict[str, Dict[str, Any]], benchmark_type: str = "entity_creation"
    ) -> Figure:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        for i, (name, data) in enumerate(datasets.items()):
            if benchmark_type in data:
                bench_data = data[benchmark_type]

                if benchmark_type == "query_performance":
                    if "single_component" in bench_data:
                        bench_data = bench_data["single_component"]
                    else:
                        continue
                elif benchmark_type == "component_operations":
                    if "add" in bench_data:
                        bench_data = bench_data["add"]
                    else:
                        continue

                entity_counts = sorted([int(k) for k in bench_data.keys()])
                times = [np.mean(bench_data[str(count)]) for count in entity_counts]

                ax1.plot(
                    entity_counts,
                    times,
                    marker="o",
                    label=name,
                    color=self.colors[i % len(self.colors)],
                    linewidth=2,
                )

                if i == 0:
                    baseline_times = times
                else:
                    speedup = [b / t for b, t in zip(baseline_times, times)]
                    ax2.plot(
                        entity_counts,
                        speedup,
                        marker="s",
                        label=f"{name} vs {list(datasets.keys())[0]}",
                        color=self.colors[i % len(self.colors)],
                        linewidth=2,
                    )

        ax1.set_xlabel("Number of Entities", fontsize=12)
        ax1.set_ylabel("Time", fontsize=12)
        title = benchmark_type.replace("_", " ").title()
        if benchmark_type == "query_performance":
            title += " (Single Component)"
        elif benchmark_type == "component_operations":
            title += " (Add Operation)"
        ax1.set_title(f"{title} - Performance Comparison", fontsize=14, fontweight="bold")
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        ax1.legend()
        self.setup_time_axis(ax1, "y")

        if len(datasets) > 1:
            ax2.set_xlabel("Number of Entities")
            ax2.set_ylabel("Speedup Factor")
            ax2.set_title("Relative Performance")
            ax2.set_xscale("log")
            ax2.axhline(y=1, color="black", linestyle="--", alpha=0.5)
            ax2.legend()
            ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def generate_report(self, data: Dict[str, Any], output_dir: Union[str, Path]) -> None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = output_dir / f"benchmark_report_{timestamp}"
        report_dir.mkdir(exist_ok=True)

        if "entity_creation" in data:
            fig = self.plot_entity_creation(data["entity_creation"])
            fig.savefig(report_dir / "entity_creation.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

        if "query_performance" in data:
            fig = self.plot_query_performance(data["query_performance"])
            fig.savefig(report_dir / "query_performance.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

        if "component_operations" in data:
            fig = self.plot_component_operations(data["component_operations"])
            fig.savefig(report_dir / "component_operations.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

        if "memory_usage" in data:
            fig = self.plot_memory_usage(data["memory_usage"])
            fig.savefig(report_dir / "memory_usage.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

        with open(report_dir / "benchmark_data.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"Benchmark report generated in: {report_dir}")


def generate_sample_data() -> Dict[str, Any]:
    np.random.seed(42)

    entity_counts = [100, 1000, 10000, 100000]

    entity_creation = {}
    for count in entity_counts:
        base_time = count * 0.00001
        times = np.random.normal(base_time, base_time * 0.1, 10).tolist()
        entity_creation[str(count)] = times

    query_performance = {"single_component": {}, "two_components": {}, "three_components": {}}

    for query_type, multiplier in [
        ("single_component", 1),
        ("two_components", 1.5),
        ("three_components", 2.2),
    ]:
        for count in entity_counts:
            base_time = count * 0.000001 * multiplier
            times = np.random.normal(base_time, base_time * 0.15, 10).tolist()
            query_performance[query_type][str(count)] = times

    component_operations = {"add": {}, "remove": {}, "get": {}}

    for op, base_multiplier in [("add", 1), ("remove", 1.2), ("get", 0.5)]:
        for count in entity_counts:
            base_time = 0.00001 * base_multiplier
            times = np.random.normal(base_time, base_time * 0.1, 10).tolist()
            component_operations[op][str(count)] = times

    memory_usage = {}
    for count in entity_counts:
        base_memory = count * 256
        memory = np.random.normal(base_memory, base_memory * 0.05, 5).tolist()
        memory_usage[str(count)] = memory

    return {
        "entity_creation": entity_creation,
        "query_performance": query_performance,
        "component_operations": component_operations,
        "memory_usage": memory_usage,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "system": "PyECS",
            "version": "0.1.0",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Generate benchmark visualizations for PyECS")
    parser.add_argument("--input", "-i", type=str, help="Path to benchmark JSON file")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="./benchmark_results",
        help="Output directory for graphs",
    )
    parser.add_argument(
        "--sample", "-s", action="store_true", help="Generate sample data for testing"
    )
    parser.add_argument("--compare", "-c", nargs="+", help="Compare multiple benchmark files")
    parser.add_argument(
        "--type",
        "-t",
        choices=[
            "entity_creation",
            "query_performance",
            "component_operations",
            "memory_usage",
            "all",
        ],
        default="all",
        help="Type of benchmark to visualize",
    )

    args = parser.parse_args()

    visualizer = BenchmarkVisualizer()

    if args.sample:
        print("Generating sample benchmark data...")
        data = generate_sample_data()
        visualizer.generate_report(data, args.output)
    elif args.compare:
        print(f"Comparing {len(args.compare)} benchmark files...")
        datasets = {}
        for filepath in args.compare:
            name = Path(filepath).stem
            datasets[name] = visualizer.load_benchmark_data(filepath)

        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        for bench_type in ["entity_creation", "query_performance", "component_operations"]:
            fig = visualizer.plot_comparison(datasets, bench_type)
            fig.savefig(output_dir / f"comparison_{bench_type}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

        print(f"Comparison plots saved to: {output_dir}")
    elif args.input:
        print(f"Loading benchmark data from: {args.input}")
        data = visualizer.load_benchmark_data(args.input)

        if args.type == "all":
            visualizer.generate_report(data, args.output)
        else:
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)

            if args.type == "entity_creation" and "entity_creation" in data:
                fig = visualizer.plot_entity_creation(data["entity_creation"])
            elif args.type == "query_performance" and "query_performance" in data:
                fig = visualizer.plot_query_performance(data["query_performance"])
            elif args.type == "component_operations" and "component_operations" in data:
                fig = visualizer.plot_component_operations(data["component_operations"])
            elif args.type == "memory_usage" and "memory_usage" in data:
                fig = visualizer.plot_memory_usage(data["memory_usage"])
            else:
                print(f"Benchmark type '{args.type}' not found in data")
                return

            fig.savefig(output_dir / f"{args.type}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)
            print(f"Plot saved to: {output_dir / f'{args.type}.png'}")
    else:
        print(
            "No input file specified. Use --sample to generate test data or --input to load a file."
        )
        parser.print_help()


if __name__ == "__main__":
    main()
