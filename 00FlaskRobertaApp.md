Create a Flask Application with RoBERTa Sequence Classification Model in a Container and Publish to Docker Hub

## Step 1: Set Up the Project

    #Create a python virtual env 
    python -m venv flask-roberta-app && cd flask-roberta-app
    
    #Activate the virtual environment:
    source bin/activate
    
    #Create a source folder.
    mkdir flask-roberta-app-ws && cd flask-roberta-app-ws

    #Create a `requirements.txt` file and add the required packages:
    simpletransformers==0.4.0
    tensorboardX==1.9
    transformers==2.1.0
    flask==1.1.2
    torch==1.7.1
    onnxruntime==1.6.0


    #Install the dependencies listed in `requirements.txt`:

    pip install -r requirements.txt
    
    #Create a WORKDIRDIR folder named webapp. 
    mkdir webapp && cd webapp
    

## Step 2: Develop the Flask Application

    
3.  Create an `app.py` file in webapp and write your Flask application code. Here's a basic example:
    

        from flask import Flask, request, jsonify 
        
        import torch
        
        import numpy as np 
        
        from transformers import RobertaTokenizer 
        
        import onnxruntime
        
        
        app = Flask(__name__)
        
        tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        
        session = onnxruntime. InferenceSession ("roberta-sequence-classification-9.onnx")
        
        
        @app.route("/predict", methods=["POST"]) 
        def predict():
        
            input_ids = torch.tensor(
                tokenizer.encode(request.json[0], add_special_tokens=True)
            ).unsqueeze(0)
    
            if input_ids.requires_grad:
                numpy_func = input_ids.detach().cpu().num()
            else:
                numpy_func = input_ids.cpu().numy()    
                
            inputs = {session.get_inputs () [0].name: numpy_ func(input_ids)}
            
            out = session.run(None, inputs)
            
            result = np. argmax (out)
            
            return jsonify({"positive": bool(result)r)
    
        if __name__ == "main":
            app.run(host="0.0.0.0", port=5000, debug=True)
            
   
4.  Download the RoBERTa-SequenceClassification (https://oreil.ly/Pjvit) ONNX model locally, and place it at the webapp folder

        curl https://github.com/onnx/models/blob/main/text/machine_comprehension/roberta/model/roberta-sequence-classification-9.onnx --output roberta-sequence-classification-9.onnx

        
    

## Step 3: Create a Dockerfile

1.  Create a file named `Dockerfile` in the project directory.
    
2.  Add the following content to the Dockerfile:

        FROM python: 3.8
        
        COPY . /requirements.txt /webapp/requirements.txt
        
        WORKDIR /webapp
        
        RUN pip install -r requirements. txt
        
        COPY webapp/* /webapp
        
        ENTRYPOINT ["python" ]
        
        CMD ["app.py"]
    

## Step 4: Build and Test the Docker Container

1.  Build the Docker container:
    
        docker build -t flask-roberta-app .

2. Double-check that the image is now available after building
    
        docker images flask-roberta-app    

3.  Run the container:
    
        docker run -p 5000:5000 flask-roberta-app
    
4.  Access your Flask app in a web browser or use a tool like `curl` to make requests to `http://localhost:5000`.
    

## Step 5: Adding a Workflow to Your Git Repository

1.  Create a GitHub Actions workflow file in the .github/workflows directory with the name build.yml
    
2.  Here's an example workflow that builds and tests the Docker container:
  

        name: Build and Test
        
        on:
          push:
            branches:
              - master
        
        jobs:
          build:
            runs-on: ubuntu-latest
        
            steps:
            - name: Checkout code
              uses: actions/checkout@v2
        
            - name: Build Docker image
              run: docker build -t flask-roberta-app .
        
            - name: Run tests
              run: docker run flask-roberta-app python -m unittest discover
        
            - name: Publish Docker image
              run: |
                echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
                docker tag flask-roberta-app ${{ secrets.DOCKER_USERNAME }}/flask-roberta-app:latest
                docker push ${{ secrets.DOCKER_USERNAME }}/flask-roberta-app:latest
              env:
                DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
                DOCKER_TOKEN: ${{ secrets.DOCKER_TOKEN }}

    The DOCKER_TOKEN secret is expected to be a Docker access token that you've created in your Docker Hub account. Access tokens are more secure for automation and can be scoped to specific actions.

    Make sure you have added the DOCKER_USERNAME and DOCKER_TOKEN secrets in your GitHub repository settings. The DOCKER_USERNAME secret should be your Docker Hub username, and the DOCKER_TOKEN secret should be the access token you've generated for Docker Hub authentication.

## Step 5: Publish to GitHub Repository

1. Configuring GitHub to Avoid Using Username and Password

    To interact with GitHub without the need for entering a username and password every time, you can configure SSH authentication. Here are the steps:

2. Generate SSH Key
    
    `ssh-keygen -t ed25519 -C "your_email@example.com"` 
   
3. Configure Git to Use SSH

    - Set your Git username and email address, and configure Git to use SSH. Use the following commands:

            git config --global user.name "Your GitHub Username"
            git config --global user.email "your_email@example.com"

4. Add SSH Key to GitHub Account

    1.  Log into your GitHub account.
    2.  Click on your profile picture → Settings → SSH and GPG keys → New SSH key.
    3.  Paste the contents of your `id_ed25519.pub` file into the "Key" field, give your key a descriptive title, and click "Add SSH key".


5. Create an Empty Repository on GitHub    

    Before you can push your code, you need to create an empty repository on GitHub:

    1. Log in to your GitHub account.
    2. Click on the "+" sign in the top right corner of the GitHub website.
    3. Select "New repository" from the dropdown menu.
    4. Give your repository a name and, optionally, a description.
    5. Choose if you want your repository to be public or private (private repositories may require a paid GitHub plan).
    6. Do not select any checkboxes for initializing the repository with README, .gitignore, or a license, as we'll push an existing repository.
    7. Click on the "Create repository" button.

6. Push Code to GitHub

    Now that you have generated an SSH key, added it to your GitHub account, configured Git to use SSH, and created an empty repository on GitHub, you can push your code to GitHub:

        # Navigate to your project directory (the directory where your code is located) 
        cd /path/to/your/project # Initialize Git (if not already initialized) 
        git init
        
        # Add the files you want to commit to the staging area 
        git add . 
        
        # Commit the changes with a meaningful message 
        git commit -m "Your commit message here" 
        
        # set remote github repository
        git remote add origin git@github.com:YourUsername/YourRepository.git
        
        # Push the committed changes to the master branch of your GitHub repository 
        git push origin master
