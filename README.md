Teammate setup, in order

1. Accept your invite. GitHub emails them. They can also find it at github.com/notifications. Until they accept, they can’t see the private repo.

2. Install the tools:

Miniforge (conda)
GitHub Desktop, signed in to their GitHub account
VS Code, plus the Python extension from Microsoft. Search “Python” in the Extensions tab.

3. Clone the repo. In GitHub Desktop: File → Clone Repository → choose hinger-asl → Clone.

4. Build the environment from your requirements.txt. In Terminal (Mac) or Miniforge Prompt (Windows):

bash
conda create -n AI-CW "python=3.12" -y
conda activate AI-CW
cd path/to/hinger-asl
pip install -r requirements.txt

5. Open the project in VS Code. In GitHub Desktop, use Repository → Open in Visual Studio Code.

6. Select the interpreter. Press Ctrl+Shift+P (Cmd+Shift+P on Mac) → Python: Select Interpreter → choose AI-CW. This is the step people forget.

7. Check it works. Run this in VS Code’s terminal:

bash
python -c "import mediapipe, sklearn; print('ready')"

If it prints ready, they can start working.