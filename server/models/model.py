from transformers import pipeline
from server.models.label import Label


class Model:
    def __init__(self, model_type: str, task: str, labels: list[Label]):
        self.model = pipeline(task, model=model_type)
        self.labels = labels

    def batch_infer():
        pass

    def infer(self, text: str):
        result = self.model(text, candidate_labels=self.labels)
        result.pop('sequence')
        return result


email_classification_model = Model(
    model_type="facebook/bart-large-mnli",
    task="zero-shot-classification",
    labels=[Label.Job, Label.NotJob],
)
