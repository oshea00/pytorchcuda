from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import openai
import spacy
import sys

# Initialize the Presidio Analyzer
# use the small model to reduce the memory usage
# download the mode as a file from https://spacy.io/usage/models#usage-import
# With external URL
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0-py3-none-any.whl
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz

# Using spacy info to get the external URL
#pip install $(spacy info en_core_web_sm --url)

# With local file
#pip install /Users/you/en_core_web_sm-3.0.0-py3-none-any.whl
#pip install /Users/you/en_core_web_sm-3.0.0.tar.gz

nlp = spacy.load("en_core_web_sm")
print (nlp._path)

from presidio_analyzer.nlp_engine import NlpEngineProvider

# Define the NLP engine and load the small spaCy model
provider = NlpEngineProvider(nlp_configuration={"nlp_engine_name": "spacy", "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]})
nlp_engine = provider.create_engine()

# Initialize the AnalyzerEngine with the specified NLP engine
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
anonymizer = AnonymizerEngine()

entities = ['PERSON', 'ORGANIZATION', 'EMAIL_ADDRESS', 'CREDIT_CARD', 'US_SSN', 'AU_ABN', 'IN_AADHAAR', 'US_DRIVER_LICENSE', 'US_PASSPORT', 
            'AU_TFN', 'US_BANK_NUMBER', 'EMAIL', 'PHONE_NUMBER', 'URL', 'CRYPTO', 'AU_ACN']

# Function to detect and mask PII in text
def mask_pii(text):
    """
    Masks personally identifiable information (PII) in the given text.

    Args:
        text (str): The text containing PII.

    Returns:
        str: The anonymized text with PII masked.

    """
    results = analyzer.analyze(text=text, entities=entities, language='en')
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_text.text


# Initialize the OpenAI API key
client = openai.OpenAI()

def load_email_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def clean_email_content(file_path):
    email_text = mask_pii(load_email_text(file_path))
    
    # Define the prompt
    prompt = f"""
    I have an email text, and I need to extract and display only the main content while 
    removing any boilerplate text such as signatures, disclaimers, or any text after the main body. 
    Here's the email text delimited by ```:
    ```
    {email_text}
    ```
    Format the email to show only the main content. Remove any signatures, disclaimers, 
    or other boilerplate text that typically appears at the end of an email.
    Do not include any text that is not part of the main body of the email.
    Do not repeat these instructions in the response.
    Do not include delimiters such as triple quotes in the response.
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role":"user","content":f"{prompt}"}],
    temperature=0.2,
    top_p=1,
    max_tokens=4096,
    stream=False
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    
    i=1
    try:
        while True:
            email_file_path = "./email/email"+str(i)+".txt"
            cleaned_email = clean_email_content(email_file_path)
            print("Cleaned Email Content:")
            print(cleaned_email)
            print("********************************************************")
            i+=1
    except Exception as e:
        print(e)
