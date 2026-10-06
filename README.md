# MovieGPT

## AI Movie & TV Show Recommendation System

MovieGPT is a local AI-powered movie and TV show recommendation application.

The system combines a **content-based recommendation engine** with a **local Large Language Model (LLM)** to understand user requests and provide movie or TV show recommendations through a desktop interface.

The recommendation system uses the Netflix titles dataset, while **Qwen 2.5 3B** is used locally through **Ollama** for natural-language intent classification.

---

## Features

- Movie and TV show recommendations
- Netflix dataset containing 8,807 titles
- Content-based recommendation system
- TF-IDF feature extraction
- Nearest Neighbors similarity search
- Natural-language title detection
- Local Qwen 2.5 3B LLM
- Intent classification
- Tkinter desktop application
- "Thinking..." state while the AI processes a request
- No cloud API key required
- Can run locally after setup

---

## Project Architecture

```text
                    MovieGPT
                       |
                 Tkinter GUI
                       |
                 User Message
                       |
                Qwen 2.5 3B
                       |
                Intent Detection
                       |
              +--------+--------+
              |                 |
           Greeting       Recommendation
              |                 |
           Response         Title Search
                                |
                           find_title()
                                |
                           recommend()
                                |
                        TF-IDF + Neighbors
                                |
                         Similar Titles
                                |
                           GUI Response
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Dataset processing |
| Scikit-learn | Machine learning and recommendation |
| TF-IDF | Text feature extraction |
| Nearest Neighbors | Similarity search |
| Ollama | Local LLM runtime |
| Qwen 2.5 3B | Natural-language intent classification |
| Tkinter | Desktop graphical interface |
| Git/GitHub | Version control |

---

# Dataset

MovieGPT uses the Netflix titles dataset.

The dataset contains:

- **8,807 titles**
- **6,131 movies**
- **2,676 TV shows**

Important fields include:

```text
type
title
director
cast
country
release_year
rating
duration
listed_in
description
```

The project also creates:

```text
duration_minutes
seasons
```

during data cleaning.

---

# How the Recommendation System Works

MovieGPT uses a **content-based recommendation system**.

Instead of recommending movies based on what other users watched, the system compares the information contained in each movie or TV show.

The following information is combined:

```text
Title
Director
Cast
Country
Genres
Description
```

For example:

```text
Blood & Water
Drama
South Africa
Teen
Mystery
School
```

This information is converted into numerical features using **TF-IDF**.

---

# TF-IDF

TF-IDF means:

**Term Frequency - Inverse Document Frequency**

It converts text into numbers so that a machine-learning algorithm can compare different titles.

For example:

```text
Movie A → [0.12, 0.00, 0.45, 0.21, ...]
Movie B → [0.10, 0.02, 0.43, 0.19, ...]
```

Titles with similar feature vectors are considered more similar.

---

# Nearest Neighbors

MovieGPT uses Scikit-learn's:

```python
NearestNeighbors
```

with:

```python
metric="cosine"
```

This allows the system to find titles whose TF-IDF representations are closest to the selected title.

For example:

```text
User:
Something like Blood & Water

MovieGPT:

1. Diamond City
2. Kings of Jo'Burg
3. How To Ruin Christmas
4. Cold Harbour
5. Shirkers
```

---

# Local LLM

MovieGPT uses:

**Qwen 2.5 3B**

as its local Large Language Model.

The model is executed using:

**Ollama**

The LLM is primarily responsible for understanding the user's **intent**.

It classifies messages into:

```text
GREETING
RECOMMENDATION
HELP
GOODBYE
```

Example:

```text
User:
Hello

Qwen:
GREETING
```

Another example:

```text
User:
I want something like Blood & Water

Qwen:
RECOMMENDATION
```

The LLM does **not** directly generate the recommendations.

The recommendation engine does that part.

This separation makes the system more reliable.

---

# Why Use a Local LLM?

The LLM runs on the user's own computer.

The application does not need:

- OpenAI API
- Gemini API
- Claude API
- API keys
- Cloud inference

The model is downloaded once through Ollama and then runs locally.

---

# Installing Ollama

Download and install Ollama on the computer.

After installation, open PowerShell and check:

```powershell
ollama --version
```

Then download the model:

```powershell
ollama pull qwen2.5:3b
```

Test the model:

```powershell
ollama run qwen2.5:3b
```

If Qwen responds, the LLM is installed correctly.

Exit the model with:

```text
/bye
```

---

# Clone the Project from GitHub

Open PowerShell.

Clone the repository:

```powershell
git clone https://github.com/chanura-madushan/MovieGPT.git
```

Enter the project:

```powershell
cd MovieGPT
```

---

# Create a Virtual Environment

Create the Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

# Install Python Requirements

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

---

# Run MovieGPT

Make sure Ollama is installed and Qwen is available:

```powershell
ollama list
```

You should see:

```text
qwen2.5:3b
```

Then run:

```powershell
python src/app.py
```

The MovieGPT desktop application will open.

---

# Example Usage

### Greeting

```text
You:
Hello
```

MovieGPT responds with a greeting.

---

### Help

```text
You:
What can you do?
```

MovieGPT explains its functionality.

---

### Recommendation

```text
You:
Something like Blood & Water
```

MovieGPT searches the dataset for the title and finds similar titles.

---

### Natural Language

The system can understand sentences such as:

```text
I want something like Blood & Water
```

or:

```text
Can you recommend something similar to Blood & Water?
```

or:

```text
I enjoyed Blood and Water, give me something similar
```

The title matching system searches for the actual title inside the user's message.

---

# Project Structure

```text
MovieGPT/
│
├── data/
│   ├── netflix_titles.csv
│   └── netflix_cleaned.csv
│
├── src/
│   ├── app.py
│   ├── chatbot.py
│   ├── cleaneddata.py
│   ├── inspectdata.py
│   ├── main.py
│   ├── recommender.py
│   └── test_qwen.py
│
├── README.md
└── requirements.txt
```

---

# Important Files

### `src/app.py`

Main desktop graphical interface.

It contains:

- Tkinter window
- Chat interface
- Input box
- Send button
- Thinking indicator
- Qwen integration
- Recommendation responses

---

### `src/recommender.py`

Contains the recommendation engine.

It handles:

- Dataset loading
- Feature creation
- TF-IDF
- Nearest Neighbors
- Title matching
- Recommendations

---

### `src/cleaneddata.py`

Cleans the original Netflix dataset.

It handles:

- Missing values
- Unnecessary columns
- Duration extraction
- Season extraction
- Clean dataset creation

---

### `src/chatbot.py`

Contains the command-line chatbot implementation.

It demonstrates the chatbot logic independently from the GUI.

---

### `src/test_qwen.py`

Used to test communication between Python and the local Qwen model through Ollama.

---

# System Requirements

Recommended:

```text
OS: Windows 10/11
RAM: 16 GB
Python: 3.10+
GPU: Optional
Storage: Several GB available
```

A GPU is not strictly required because Qwen can run using the CPU, although a compatible GPU can improve inference performance.

---

# Important Note About Git

The Qwen model itself should **not** be uploaded to GitHub.

The model is several GB in size and is managed by Ollama.

GitHub stores:

```text
Python code
Dataset
README
Requirements
Project files
```

Ollama downloads:

```text
Qwen 2.5 3B
```

Therefore, after cloning the GitHub repository on a new computer, run:

```powershell
ollama pull qwen2.5:3b
```

Then:

```powershell
pip install -r requirements.txt
```

and finally:

```powershell
python src/app.py
```

---

# Project Goal

The goal of MovieGPT is to demonstrate how a traditional machine-learning recommendation system can be combined with a local Large Language Model to create an interactive AI application.

The LLM handles natural-language understanding, while the recommendation engine performs the actual similarity-based recommendation.

---

# Author

**Chanura Madushan**

MovieGPT — AI Movie & TV Show Recommendation System
