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
    
    def formatUserData(self, inputData: dict) -> str:
        userPrompt = f"""Generate Cover Letter using this information:
        Job Title: {inputData['Job Title']}, Preferred Qualifications: {inputData['Preferred Qualifications']}, Hiring Company: {inputData['Hiring Company']}, Applicant Name: {inputData['Applicant Name']}, Past Working Experience: {inputData['Past Working Experience']}, Current Working Experience: {inputData['Current Working Experience']}, Skillsets:{inputData['Skillsets']}, Qualifications: {inputData['Qualifications']}""" 

        return userPrompt
    
    def inference(self, userPrompt: str) -> str:
        print("begining model query")
        messages = [self.systemPrompt, 
                    {'content': userPrompt,
                     'role' : 'user'}]
        print(messages)
        
        resultBatch = self.pipe(messages, **self.generation_args)

        print(resultBatch[0]['generated_text'][2]['content'])

        return (resultBatch[0]['generated_text'][2]['content'])

model = LlmModel() 