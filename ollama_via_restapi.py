from flask import Flask, request, jsonify
import subprocess
import torch
import time

app = Flask(__name__)

def check_device():
    """
    Check if a GPU is available and measure the time taken.
    Return the device type ('cuda' or 'cpu') and the elapsed time.
    """
    start_time = time.time()
    if torch.cuda.is_available():
        device = "cuda"
        gpu_name = torch.cuda.get_device_name(torch.cuda.current_device())
    else:
        device = "cpu"
        gpu_name = "No GPU available"
    elapsed_time = time.time() - start_time
    return device, gpu_name, elapsed_time


def query_ollama(prompt, genre):
    """
    Interact with the locally installed Ollama 3.2 model and measure response time.
    Args:
        prompt (str): The input text to query the model.
        genre (str): The genre or tone in which the response should be generated.
    Returns:
        str: The response from Ollama.
    """
    try:
        # Command to interact with Ollama (you can specify genre or style in the prompt)
        command = ["ollama", "run", "llama3.2"]
        prompt_with_genre = f"Explain the concept of {prompt} using a {genre} perspective." # Modify the prompt to include the genre
        start_time = time.time()

        # Running subprocess and capturing output
        process = subprocess.run(
            command,
            input=prompt_with_genre,  # Pass the modified prompt with genre
            text=True,
            capture_output=True,
            check=True,
            encoding="utf-8"  # Explicitly set encoding to UTF-8
        )

        elapsed_time = time.time() - start_time
        return process.stdout.strip(), elapsed_time

    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip() or 'Unknown error occurred'}", 0
    except FileNotFoundError:
        return "Error: Ollama is not installed or not in PATH.", 0


@app.route('/device', methods=['GET'])
def get_device_info():
    """
    Endpoint to check if the system is using a GPU or CPU.
    """
    device, gpu_name, device_time = check_device()
    return jsonify({
        "device": device,
        "gpu_name": gpu_name,
        "time_taken": f"{device_time:.4f} seconds"
    })


@app.route('/query', methods=['POST'])
def query():
    """
    Endpoint to query Ollama with a topic and genre (style).
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        genre = data.get('genre')

        # Validate inputs
        if not prompt or not genre:
            return jsonify({"error": "Both 'prompt' and 'genre' are required."}), 400

        response, response_time = query_ollama(prompt, genre)
        return jsonify({
            "response": response,
            "response_time": f"{response_time:.4f} seconds"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
