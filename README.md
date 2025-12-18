# Python-standalone-code-to-generate-mcqs
AI-Based MCQ Generator from PDFs

A Python application that extracts text from PDF files and generates multiple-choice questions (MCQs) using Google’s Gemini language model, with file-based caching to reduce repeated API calls.

Tech Stack

Python, pdfplumber, Google Generative AI (Gemini), JSON, File Caching

Key Highlights

Extracts text from multi-page PDFs.

Generates MCQs with four options, correct answer, and reference.

Implements hashing and caching to improve efficiency and reduce API usage.

Includes error handling for PDF parsing and API responses.

Usage

Run the script with a PDF file to automatically generate MCQs from the document content.
