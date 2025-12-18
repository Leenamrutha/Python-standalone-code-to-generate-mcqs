# Python-standalone-code-to-generate-mcqs
AI-Based MCQ Generator from PDFs

A Python application that extracts text from PDF files and generates multiple-choice questions (MCQs) using Google’s Gemini language model, with file-based caching to reduce repeated API calls.

## Tech Stack

Python, pdfplumber, Google Generative AI (Gemini), JSON, File Caching

## Key Highlights

1.Extracts text from multi-page PDFs.

2.Generates MCQs with four options, correct answer, and reference.

3.Implements hashing and caching to improve efficiency and reduce API usage.

4.Includes error handling for PDF parsing and API responses.

## Usage

Run the script with a PDF file to automatically generate MCQs from the document content.
