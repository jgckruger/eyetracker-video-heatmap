# eyetracker-video-heatmap
Creates heatmaps for videos from eyetracker data.

# Running the code 
You can use the built-in helper to chek how to run this program
```
python main.py
```
The main usage is ```python PATH_TO_CSV_FILE.csv PATH_TO_INPUT_VIDEO.mp4 PATH_TO_OUTPUT_VIDEO.mp4```

For example
```
python main.py .\example\text_input\in.csv '.\example\video_input\in.mp4' .\example\video_output\out.mp4
```

# Installing dependencies
It's recommended that you create a new venv before installing
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

You can install the dependencies using pip
```
pip install -r requirements.txt
```

# Building
This repo uses pyinstaller for building. You need to build the application in the respective OS you need to run it (Linux/Mac/Windows)
```
pyinstaller main.py
```