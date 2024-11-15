from transformers import pipeline 
 
class LlmModel():
    def __init__(self):
        self.__modelName = "Qwen/Qwen2.5-0.5B-Instruct"

        # load model 
        self.__pipe = pipeline("text-generation", self.__modelName, torch_dtype="auto", device_map="auto")
        self.__pipe.tokenizer.padding_side="left"

        # system prompt for model 
        self.__systemPrompt = {'content': 
                             'You are a helpful assistant who writes tailored Cover Letters.',
                            'role': 'system'}
        
        # initalise optimised generation arguments 
        self.__generation_args = {
            "max_new_tokens": 512,
            "batch_size": 2,
            "temperature": 0.7,
            "top_k": 20,
            "top_p": 0.8,
        }

        print("***Qwen2.5-0.5B-Instruct LLM model Initalised****")
    
    # query model 
    def inference(self, userPrompt: str) -> str:
        print("begining model query")
        messages = [self.__systemPrompt, 
                    {'content': userPrompt,
                     'role' : 'user'}]
        
        resultBatch = self.__pipe(messages, **self.__generation_args)
        
        # return just the cover letter 
        return (resultBatch[0]['generated_text'][2]['content'])

# initalise model 
model = LlmModel() 