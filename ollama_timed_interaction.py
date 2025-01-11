import subprocess
import time

def query_ollama(topic, genre):
    """
    Interact with the locally installed Ollama 3.2 model and measure response time.
    Args:
        topic (str): The input text/topic to query the model.
        genre (str): The genre or perspective to explain the topic in.
    Returns:
        str: The response from Ollama.
    """
    try:
        prompt = f"Explain the concept of {topic} using a {genre} perspective."
        command = ["ollama", "run", "llama3.2"]

        # Running subprocess and capturing output
        start_time = time.time()
        process = subprocess.run(
            command,
            input=prompt,  # Pass the prompt as input
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

def main():
    print("Ollama 3.2 Local Interaction")
    
    while True:
        topic = input("Enter the topic you want to know about: ")
        genre = input("Enter the genre you want to get it in (e.g., cricket, football, physics, etc.): ")
        
        if topic.lower() == "exit" or genre.lower() == "exit":
            print("Exiting...")
            break

        response, response_time = query_ollama(topic, genre)
        print(f"Ollama: {response}")
        print(f"Response generated in {response_time:.4f} seconds.\n")

if __name__ == "__main__":
    main()
