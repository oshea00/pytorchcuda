import openai
import sys

# Initialize the OpenAI API key
client = openai.OpenAI()

def load_email_text(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def clean_email_content(file_path):
    email_text = load_email_text(file_path)
    
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
    except:
        pass
