import time

def stream_text(text, delay=0.02):
    """Generator function to simulate typewriter effect."""
    for char in text.split(" "):
        yield char + " "
        time.sleep(delay)

def generate_skeleton_loader():
    """Returns HTML for a skeleton loader animation."""
    return """
    <div style="
        width: 100%;
        height: 20px;
        background: linear-gradient(90deg, #1f1f1f 25%, #2a2a2a 50%, #1f1f1f 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 4px;
        margin-bottom: 10px;
    "></div>
    <style>
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    """
