# Health System Navigator

Health System Navigator is an AI-powered web platform that simplifies the process of finding the right doctor based on personal preferences, symptoms, and insurance details—saving patients hours of time and stress.

## Features

- AI-driven symptom intake with follow-up questions
- Smart doctor recommendations based on:
  - Location
  - Specialization
  - Insurance provider
  - Gender and language preferences
- Local RAG (Retrieval-Augmented Generation) implementation for multi-turn queries
- Appointment booking support
- Privacy-focused (RAG model saved and queried locally)

## Tech Stack

- **Frontend**: Flask + HTML/CSS
- **Backend**: Python, Pandas
- **Model**: OpenBioLLM-8B (8-bit quantized) via llama-cpp-python
- **Deployment**: Vercel
- **Data Source**: National Provider Identifier Registry (cleaned ~770k+ U.S. doctors)

## Getting Started

Coming soon: setup instructions for local development and model hosting.
