# ==============================
# JOKE GENERATOR APP
# ==============================
# This app fetches random jokes from an external API
# and displays them with a clean UI
# ==============================

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import httpx
import asyncio

# ==============================
# CREATE APP
# ==============================
app = FastAPI()

# ==============================
# EXTERNAL API
# ==============================
# Using JokeAPI: https://jokeapi.dev/
JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any"

# ==============================
# HTML FRONTEND
# ==============================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>🤣 Joke Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }

        .joke-box {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .joke-text {
            font-size: 1.2em;
            color: #333;
            text-align: center;
            line-height: 1.6;
        }

        .joke-setup {
            font-weight: bold;
            margin-bottom: 10px;
            color: #667eea;
        }

        .joke-delivery {
            margin-top: 10px;
            color: #555;
            font-style: italic;
        }

        .loading {
            text-align: center;
            color: #999;
            font-size: 1.1em;
        }

        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 10px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button:active {
            transform: translateY(0);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .joke-type {
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-top: 10px;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #c33;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🤣 Joke Generator</h1>
    
    <div class="joke-box">
        <div id="joke-content" class="joke-text loading">
            Click the button to get a joke!
        </div>
    </div>

    <button onclick="getJoke()" id="joke-btn">Get a Joke 😄</button>
    <button onclick="getJoke()" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">Another One! 🎉</button>

    <div class="joke-type" id="joke-type"></div>
</div>

<script>
// ==============================
// FETCH JOKE FROM API
// ==============================
async function getJoke() {
    const btn = document.getElementById("joke-btn");
    const content = document.getElementById("joke-content");
    const typeDiv = document.getElementById("joke-type");

    btn.disabled = true;
    content.innerHTML = '<div class="loading">Loading joke...</div>';
    typeDiv.innerHTML = '';

    try {
        const response = await fetch("/api/joke");
        const data = await response.json();

        if (data.error) {
            content.innerHTML = `<div class="error">❌ ${data.error}</div>`;
        } else {
            let jokeText = '';
            
            if (data.type === 'single') {
                jokeText = data.joke;
            } else {
                jokeText = `
                    <div class="joke-setup">${data.setup}</div>
                    <div class="joke-delivery">${data.delivery}</div>
                `;
            }

            content.innerHTML = jokeText;
            typeDiv.innerHTML = `📌 Category: ${data.category} | Type: ${data.type === 'single' ? 'Single' : 'Setup & Delivery'}`;
        }
    } catch (error) {
        content.innerHTML = `<div class="error">❌ Failed to fetch joke: ${error.message}</div>`;
    } finally {
        btn.disabled = false;
    }
}

// Load a joke when page loads
getJoke();
</script>

</body>
</html>
"""

# ==============================
# ROUTES
# ==============================

@app.get("/", response_class=HTMLResponse)
def home():
    """Serve the main HTML page"""
    return HTML_PAGE


@app.get("/api/joke")
async def get_joke():
    """Fetch a random joke from JokeAPI"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(JOKE_API_URL)
            response.raise_for_status()
            joke_data = response.json()

            # Handle the response from JokeAPI
            if joke_data.get("error"):
                return {"error": "Could not fetch joke at this moment"}

            return {
                "type": joke_data.get("type"),  # "single" or "twopart"
                "category": joke_data.get("category"),
                "joke": joke_data.get("joke"),  # For single jokes
                "setup": joke_data.get("setup"),  # For two-part jokes
                "delivery": joke_data.get("delivery"),  # For two-part jokes
            }

    except Exception as e:
        return {"error": f"Failed to fetch joke: {str(e)}"}


# ==============================
# RUN INSTRUCTIONS
# ==============================
# Save this file as: joke_generator.py
# Then run:
# pip install fastapi uvicorn httpx
# uvicorn joke_generator:app --reload
#
# Open browser:
# http://127.0.0.1:8000
# ==============================
