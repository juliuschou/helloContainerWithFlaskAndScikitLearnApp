Task 1: Create a Flask Application with RoBERTa Sequence Classification Model in a Container and Publish to Docker Hub

Step 1: Set Up the Project

1.  Create a new directory for your project:
    
    `mkdir flask-roberta-app` 
    
2.  Navigate into the project directory:
    
    `cd flask-roberta-app` 
    
3.  Initialize a Git repository:
    
    `git init` 
    
4.  Create a virtual environment:
    
    `python -m venv venv` 
    
5.  Activate the virtual environment:
    
    -   On Windows: `venv\Scripts\activate`
    -   On macOS and Linux: `source venv/bin/activate`

Step 2: Develop the Flask Application

1. Create a `requirements.txt` file and add the required packages:

    simpletransformers==0.4.0
    tensorboardX==1.9
    transformers==2.1.0
    flask==1.1.2
    torch==1.7.1
    onnxruntime==1.6.0

2. Install the dependencies listed in `requirements.txt`:

    pip install -r requirements.txt

    
3.  Create an `app.py` file and write your Flask application code. Here's a basic example:
    

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
            
   
4.  Download the RoBERTa-SequenceClassification (https://oreil. ly/Pjvit) ONNX model locally, and place it at the root of the project

    curl https://github.com/onnx/models/blob/main/text/machine_comprehension/roberta/model/roberta-sequence-classification-9.onnx --output roberta-sequence-classification-9.onnx

        
    

Step 3: Create a Dockerfile

1.  Create a file named `Dockerfile` in the project directory.
    
2.  Add the following content to the Dockerfile:

        FROM python: 3.8
        
        COPY . /requirements.txt /webapp/requirements.txt
        
        WORKDIR /webapp
        
        RUN pip install -r requirements. txt
        
        COPY webapp/* /webapp
        
        ENTRYPOINT ["python" ]
        
        CMD ["app.py"]
    

Step 4: Build and Test the Docker Container

1.  Build the Docker container:
    
    `docker build -t flask-roberta-app .` 
    
2.  Run the container:
    
    `docker run -p 5000:5000 flask-roberta-app` 
    
3.  Access your Flask app in a web browser or use a tool like `curl` to make requests to `http://localhost:5000`.
    

Step 5: Publish to GitHub Repository

1.  Create a new repository on GitHub.
    
2.  Link your local Git repository to the remote GitHub repository:
    
    csharpCopy code
    
    `git remote add origin <repository-url>` 
    
3.  Commit and push your code to GitHub:
    
    
    git add .
    git commit -m "Initial commit"
    git push -u origin master
    

Step 6: Add GitHub Actions for Build Verification

1.  In your GitHub repository, navigate to the "Actions" tab and create a new workflow.
    
2.  Define the workflow using a YAML file (e.g., `.github/workflows/build.yml`). Here's an example workflow that builds and tests the Docker container:
  

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
