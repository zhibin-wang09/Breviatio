from transformers import pipeline
from server.models.label import Label


class Model:
    def __init__(self, model_type: str, task: str):
        self.model = pipeline(task, model=model_type)

    def batch_infer():
        pass

    def infer(self, text: str):
        result = self.model(text, max_length = 130, min_length = 40)
        return result


email_summarization_model = Model(
    model_type="facebook/bart-large-cnn",
    task="summarization",
)
