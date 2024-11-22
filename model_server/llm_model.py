from transformers import pipeline
import logging 
 
class LlmModel():
    def __init__(self):
        self.__modelPath = "/model/Qwen2.5-0.5B-Instruct"
        self.__modelName = "Qwen/Qwen2.5-0.5B-Instruct"
    
        try:
            self.__pipe = pipeline("text-generation", self.__modelPath, torch_dtype="auto", device="cpu")
            print("***Qwen2.5-0.5B-Instruct Model Loaded in Locally***")
        except:
            # download model 
            print("***Downloading Qwen2.5-0.5B-Instruct LLM model from HuggingFace***")
            self.__pipe = pipeline("text-generation", self.__modelName, torch_dtype="auto", device="cpu")
            self.__pipe.save_pretrained(self.__modelPath)

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

        print("***Qwen2.5-0.5B-Instruct LLM model Initalised***")
    
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
