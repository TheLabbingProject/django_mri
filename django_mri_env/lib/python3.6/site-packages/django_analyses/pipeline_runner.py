from django.db.models import QuerySet
from django_analyses.models.pipeline.node import Node
from django_analyses.models.pipeline.pipe import Pipe
from django_analyses.models.pipeline.pipeline import Pipeline


class PipelineRunner:
    def __init__(self, pipeline: Pipeline, inputs: dict):
        self.pipeline = pipeline
        self.inputs = inputs
        self.runs = {node: None for node in pipeline.node_set}

    def get_input_pipes(self, node: Node) -> QuerySet:
        return self.pipeline.pipe_set.filter(destination=node)

    def get_destination_kwarg(self, pipe: Pipe) -> dict:
        return {
            pipe.destination_port.key: [
                output.value
                for output in self.runs[pipe.source].output_set
                if output.definition.key == pipe.source_port.key
            ][0]
        }

    def get_node_inputs(self, node: Node) -> dict:
        input_pipes = self.get_input_pipes(node)
        input_kwargs = [self.get_destination_kwarg(pipe) for pipe in input_pipes]
        return {
            key: value
            for input_kwarg in input_kwargs
            for key, value in input_kwarg.items()
        }

    def run_entry_nodes(self) -> None:
        for node in self.pipeline.entry_nodes:
            node_inputs = self.inputs.get(node, self.inputs)
            self.runs[node] = node.run(node_inputs)

    def has_required_runs(self, node: Node) -> bool:
        required_runs = [
            self.runs[required_node] for required_node in node.required_nodes
        ]
        return all(required_runs)

    def run_node(self, node: Node) -> None:
        node_inputs = self.get_node_inputs(node)
        self.runs[node] = node.run(node_inputs)

    def run(self):
        self.run_entry_nodes()
        while self.pending_nodes:
            for node in self.pending_nodes:
                if self.has_required_runs(node):
                    self.run_node(node)
        return self.runs

    @property
    def pending_nodes(self) -> list:
        return [key for key in self.runs if not self.runs[key]]
