from transformers import pipeline
from . import Label

class Model():
    def __init__(self, model_type: str, task: str, labels: list[Label]):
        self.model = pipeline(task, model=model_type);
        self.labels  = labels;

    def batch_infer():
        pass

    def infer(self, text: str):
        return self.model(text, candidate_labels = self.labels);
