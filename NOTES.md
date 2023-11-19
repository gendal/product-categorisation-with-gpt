Initial Creation of environment:

```
conda create --name openai
conda activate openai
conda install -c conda-forge openai
```

Before using it thereafter 

```
conda activate openai:
```

OpenAI SDK needs API key to be set in the environment variable OPENAI_API_KEY. 

The advice is to store it in a `.env` file, that is protected by `.gitignore`. 
Remember to source it before running the code. 

```
OPENAI_API_KEY=xxxxxxx
```