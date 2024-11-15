# formats dictionary of data to userprompt to query LLM

def formatPrompt(inputData: dict) -> str:
        userPrompt = f"""Generate Cover Letter using this information:\nJob Title: {inputData['Job Title']}, Preferred Qualifications: {inputData['Preferred Qualifications']}, Hiring Company: {inputData['Hiring Company']}, Applicant Name: {inputData['Applicant Name']}, Past Working Experience: {inputData['Past Working Experience']}, Current Working Experience: {inputData['Current Working Experience']}, Skillsets:{inputData['Skillsets']}, Qualifications: {inputData['Qualifications']}""" 
        return userPrompt
