# formats dictionary of data to userprompt to query llm 

def formatPrompt(inputData: dict) -> str:
        userPrompt = f"""Generate Cover Letter using this information:\nJob Title: {inputData['Job Title']}, Preferred Qualifications: {inputData['Preferred Qualifications']}, Hiring Company: {inputData['Hiring Company']}, Applicant Name: {inputData['Applicant Name']}, Past Working Experience: {inputData['Past Working Experience']}, Current Working Experience: {inputData['Current Working Experience']}, Skillsets:{inputData['Skillsets']}, Qualifications: {inputData['Qualifications']}""" 
        return userPrompt


"""
Generate Cover Letter using this information:\\nJob Title:  Data Scientist, Preferred Qualifications: BSc focused on data Science/computer Science/engineering\\n4+ years experience Developing and shipping production grade machine learning systems\\n2+ years building and shipping data Science based personalization services and recommendation systems\\nexperience in data Science or machine learning engineering\\nStrong analytical and data Science skills, Hiring Company: XYZ Corporation, Applicant Name: John Smith, Past Working Experience: Data Analyst at ABC Company, Current Working Experience: Machine Learning Engineer at DEF Company, Skillsets:Python, R, scikit-learn, Keras, Tensorflow, Qualifications: BSc in Computer Science, 5+ years of experience in data science and machine learning

"""