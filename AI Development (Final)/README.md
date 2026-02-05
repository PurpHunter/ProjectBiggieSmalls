# Federated Mental Health & Fitness AI

This project implements an offline-first, privacy-preserving AI system
combining mental health, fitness, and nutrition support.

## Key Features
- Federated learning (no raw data leaves devices)
- Per-user memory with strict isolation
- Mental health crisis escalation
- Offline LLM inference using Ollama
- Modular, auditable architecture

## Architecture
- Devices train locally on private data
- Central federated server aggregates models
- AI runtime server handles chat & memory
- No internet dependency

## Safety
- Crisis keyword detection
- Non-diagnostic responses
- Explicit escalation guidance

## How to Run
1. Start federated server
2. Train devices locally
3. Export global model
4. Run AI server
5. Chat via `/chat` endpoint

## Intended Use
Research, education, and human-support augmentation.
Not a replacement for professional care.
