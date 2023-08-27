from transformers import pipeline

# Various Huggingface pipeline examples 

classifier = pipeline("ner", grouped_entities=True)
print(classifier("My name is Mike and I was interested in a Berkley course I could take from my home near Seattle"))


classifier = pipeline("sentiment-analysis")
print(classifier([
    "This is an awesome tool",
    "Yucky tool only a fool could love",
    "Very complicated tooling",
    "Richly featured library",
]))


classifier = pipeline("zero-shot-classification")
print(classifier("This is a review on Star Wars literature",candidate_labels=["education","movies","business"]))

generator = pipeline("text-generation", model="distilgpt2")
print(generator("In this course we will teach you how to",max_length=60,num_return_sequences=2))

question_answerer = pipeline("question-answering")
print(question_answerer(question="Where do I work?",context="My name is Mike and I often commute into Seattle to Morgan Stanley"))



