#!/bin/bash

set -e

echo "PyECS Docker Benchmark Runner"
echo "============================"

if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

SCENARIO=""
CLEAN=false
VISUALIZE=true
BUILD=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --scenario)
            SCENARIO="$2"
            shift 2
            ;;
        --no-build)
            BUILD=false
            shift
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        --no-viz)
            VISUALIZE=false
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --scenario <name>  Run specific scenario (high/medium/low/stress)"
            echo "  --no-build        Skip Docker image build"
            echo "  --clean           Clean benchmark results before running"
            echo "  --no-viz          Skip visualization generation"
            echo "  --help            Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

mkdir -p ../benchmark_results

if [ "$CLEAN" = true ]; then
    echo "Cleaning previous benchmark results..."
    rm -rf ../benchmark_results/*.json
    rm -rf ../benchmark_results/comparison
    rm -rf ../benchmark_results/benchmark_report_*
fi

if [ "$BUILD" = true ]; then
    echo "Building Docker image..."
    docker-compose -f docker-compose.benchmark.yml build
fi

if [ -n "$SCENARIO" ]; then
    echo "Running benchmark scenario: $SCENARIO"
    docker-compose -f docker-compose.benchmark.yml run --rm benchmark-$SCENARIO
else
    echo "Running all benchmark scenarios..."
    
    echo -e "\n1. High Performance (no limits)"
    docker-compose -f docker-compose.benchmark.yml run --rm benchmark-high
    
    echo -e "\n2. Medium Performance (2 CPU, 2GB RAM)"
    docker-compose -f docker-compose.benchmark.yml run --rm benchmark-medium
    
    echo -e "\n3. Low Performance (1 CPU, 512MB RAM)"
    docker-compose -f docker-compose.benchmark.yml run --rm benchmark-low
    
    echo -e "\n4. Stress Test (0.5 CPU, 256MB RAM)"
    docker-compose -f docker-compose.benchmark.yml run --rm benchmark-stress
fi

if [ "$VISUALIZE" = true ] && [ -z "$SCENARIO" ]; then
    echo -e "\nGenerating comparison visualizations..."
    docker-compose -f docker-compose.benchmark.yml run --rm visualizer
fi

echo -e "\nBenchmark Results:"
echo "=================="
ls -la ../benchmark_results/*.json 2>/dev/null || echo "No JSON results found"

if [ -d "../benchmark_results/comparison" ]; then
    echo -e "\nComparison plots generated in: benchmark_results/comparison/"
    ls -la ../benchmark_results/comparison/*.png 2>/dev/null || echo "No comparison plots found"
fi

echo -e "\nDone! To view specific results:"
echo "  cat benchmark_results/<scenario>_perf.json | jq '.metadata'"
echo "  open benchmark_results/comparison/*.png"