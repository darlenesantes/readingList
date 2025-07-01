#Here we'll call the GenAI API to generate book summaries based on the book information retrieved from the Google Books API
# Importing libraries to be used for loading the API
from google import genai
from config import GEMINI_API_KEY

# Setting API key
api_key = GEMINI_API_KEY

# Configure the client
client = genai.Client(api_key=api_key)

# Creating function to generate summary based on title and author
def generate_summary(title, author):
    '''
    Generates the summary of a book based on title and author using GenAI
    '''
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate a 1-3 sentence summary of the book {title} by {author}"
    )
    return response.text

# Quick test to ensure it works as expected:
def main():
    '''
    Main function to test the generate_summary function with sample book data.
    '''
    title = "The Hunger Games"
    author = "Suzanne Collins"

    print(generate_summary(title, author))


if __name__ == "__main__":
    main()
