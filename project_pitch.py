'''
Name of Project - Smart Book Club Manager

What problem are you solving?
a. 2 sentences
Allows us to have centralized platform to manage reading lists as well as access summaries.

Who / What does the project interface with?
a. People? People who want to search for books and make reading lists
b. other systems? (APIs) It will take information from Google Books & the Google GenAI API
c. Hardware? None

What are the inputs? 
- Search query - book isbn or title

What are the outputs? 
- Search results that match the title of the book & its author, ai-generated review/summary

List 5 steps to go from input -> output
- User would enter a search term - get a call to the google books api (parse info to get title, author) - display short summary of book
- User can add book to list (list stored as table in reading list database)
- google genai will generate description for book as attribute in its table entry
- When user wants to view the list, the table is returned with the book title, author, & description

What’s the biggest risk? 
- Inconsistent or incomplete data in Google Books API or wrong description provided by gen AI due to similar book/author names

How will you know you’re successful?
- Users can search for books, add books to their reading lists, and see the correctly generated ai summary for the book when they view their reading list

'''
