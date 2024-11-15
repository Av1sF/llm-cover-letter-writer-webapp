from transformers import pipeline 
 
class LlmModel():
    def __init__(self):
        self.modelName = "Qwen/Qwen2.5-0.5B-Instruct"
        self.pipe = pipeline("text-generation", self.modelName, torch_dtype="auto", device_map="auto")
        self.pipe.tokenizer.padding_side="left"

        self.systemPrompt = {'content': 
                             'You are a helpful assistant who writes tailored Cover Letters.',
                            'role': 'system'}
        self.generation_args = {
            "max_new_tokens": 512,
            "batch_size": 2,
            "temperature": 0.7,
            "top_k": 20,
            "top_p": 0.8,
        }
        print("Qwen2.5-0.5B-Instruct Initalised")
    
    def inference(self, userPrompt: str) -> str:
        print("begining model query")
        messages = [self.systemPrompt, 
                    {'content': userPrompt,
                     'role' : 'user'}]
        
        resultBatch = self.pipe(messages, **self.generation_args)
        
        return (resultBatch[0]['generated_text'][2]['content'])

model = LlmModel() 