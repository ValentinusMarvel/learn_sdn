import json

from benchmark_core import BenchmarkConfig, benchmark_records, build_topology_graph


def test_ring5_graph_has_host_attachments():
    config = BenchmarkConfig(topologies=("ring5",), algorithms=("astar",))
    graph = build_topology_graph("ring5", config)

    assert "s1" in graph.switch_names
    assert "h1" in graph.host_names
    assert graph.host_attachments["h1"][0] == "s1"
    assert any(neighbour == "s2" for neighbour, _ in graph.adjacency["s1"])


def test_jellyfish_graph_has_host_attachments_and_weights():
    config = BenchmarkConfig(topologies=("jellyfish",), algorithms=("astar",), default_bandwidth_mbps=100.0)
    graph = build_topology_graph("jellyfish", config)

    assert "s0" in graph.switch_names
    assert "h0" in graph.host_names
    assert graph.host_attachments["h0"][0] == "s0"
    assert len(graph.weights) > 0
    for link, weight in graph.weights.items():
        assert weight == 100.0


def test_benchmark_records_include_expected_fields():
    config = BenchmarkConfig(topologies=("ring5",), algorithms=("astar",), repetitions=1)
    record = next(benchmark_records(config))

    assert record["topology"] == "ring5"
    assert record["algorithm"] == "astar"
    assert record["status"] == "success"
    assert isinstance(record["path_switches"], list)
    assert record["source_switch"] != record["destination_switch"]
    assert record["runtime_ms"] >= 0
    assert "run_id" in record
    assert isinstance(record["run_id"], str)
    assert record["run_id"].startswith("run_graph_")


def test_records_are_json_serialisable():
    config = BenchmarkConfig(topologies=("ring5",), algorithms=("widest_path",), repetitions=1)
    record = next(benchmark_records(config))

    json.dumps(record)
