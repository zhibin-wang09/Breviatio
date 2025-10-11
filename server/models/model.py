from ollama import chat
from ollama import ChatResponse
from server.models.label import EmailCategory


class Model:
    def __init__(self, model_type: str):
        system_prompt = {'role' : 'system', 
                        'content': f'You are a helpful email butler that helps the user classify emails. We have {[e.value for e in EmailCategory]} categories. Read the email given to you and match it to one of the categories.'}
        def model_init(messages):
            # print(messages)
            response: ChatResponse = chat(model = model_type, messages = [
                system_prompt,
                {'role' : 'user', 'content': f"{messages}"}
            ])

            return response
        
        self.model = model_init
        
    def batch_infer(self, messages):
        labels = []
        for m in messages:
            label = self.infer(m)
            labels.append(label)
        return labels

    def infer(self, text: str):
        result = self.model(text)
        return result


email_categorize = Model(
    model_type="mistral"
)
