# Automatic Short Answer Grading (ASAG) System

This is the official repo for **Automatic Short Answer Grading (ASAG)** project from **Xi'an Jiaotong Liverpool University (XJTLU)**. 

Using [vLLM](https://github.com/vllm-project/vllm) as the Large Language Model (LLM) inference framework and [FastAPI](https://github.com/tiangolo/fastapi) as the HTTP service framework, this project can achieve high throughput of both LLM tokens delivered and request handling.

## Feature

This project aims to achieve high concurrency automatic short answer grading (ASAG) system and implement the construction of service.

* vLLM supports Continuous batching of incoming requests, using an extra thread for inferencing.
* vLLM provides abstracts of asyncio, using asyncio http framework after abstracts of uvicorn+FastAPI to achieve http api privision.
* vLLM stream response of next token, providing chunk streaming response based on FastAPI.

## Supported models

* `Qwen/Qwen1.5-14B-Chat-GPTQ-Int4`
* `Qwen/Qwen1.5-32B-Chat-AWQ`
* `internlm/internlm2-chat-7b`
* `01-ai/Yi-1.5-9B-Chat`
* `modelscope/Yi-1.5-34B-Chat-AWQ`
* `CohereForAI/aya-23-8B`
* `meta-llama/Meta-Llama-3-8B-Instruct`
* `THUDM/glm-4-9b-chat`
* `Qwen/Qwen2-7B-Instruct`
* `Gemma-1.1-7B`
* `Mistral-7B-v0.3`
* `Phi3-small`
* `MiniCPM-2B`

## Getting Started

### Requirements

> [!IMPORTANT] 
>
> The requirement below is mandatory. And we've only tested our project on the following platform.

| Mandatory     | Recommended |
| ------------- | ----------- |
| Python        | 3.8         |
| CUDA          | 12.1        |
| torch         | 2.1         |
| einops        | 0.8.0       |
| transformers  | 4.41.0      |
| accelerate    | 0.30.1      |
| vLLM          | 0.4.3       |
| tiktoken      | 0.6.0       |
| sentencepiece | 0.2.0       |
| scipy         | 1.13.0      |
| FastAPI       | 0.111.0     |

> [!TIP]
>
> Use `pip install -r requirement.txt` to install all the requirement.

### Quickstart

We first need to setup server-side to provide the service to the clients. To launch our HTTP server, simply:

```text
python vllm_server.py -m [index of the model in the above list]
```

After that, we can either start the student entry or client side to pass our inputs to the server:

* **For student entry:**

> [!NOTE]
>
> `0` stands for using zero-shot prompt, while `1` for one-shot, and `2` for few-shot.

```text
python student_entry.py -n [0, 1, 2]
```

* **For casual client:**

> [!NOTE]
>
> `-s` stands for get response in a streaming way, which is optional.

```text
python student_entry.py [-s]
```

**WebUI**:

After launching vllm_server, you can also run gradio_webui.py which is a webui based on gradio. This can achieve a chat-liked format like ChatGPT, which is more user-friendly.

```
python gradio_webui.py
```

![webui](https://s2.loli.net/2024/06/11/duwy9Q4j7JM1PVp.png)

## Data and Results

* Example data: [example.json](https://github.com/BiboyQG/ASAG/blob/master/data/example.json)

* Zero-shot pormpt template:

![image-20240611154055447](https://s2.loli.net/2024/06/11/8UOoJBshVgtKS1l.png)

* Test on different LLMs with prompt template and example data: [results](https://github.com/BiboyQG/ASAG/tree/master/results).

## Acknowledgement

* Online inference: [vllm_server.py](https://github.com/BiboyQG/ASAG/blob/master/vllm_server.py) referenced from [vLLM official implementation - server](https://github.com/vllm-project/vllm/blob/main/vllm/entrypoints/api_server.py).
* Online inference: [vllm_client.py](https://github.com/BiboyQG/ASAG/blob/master/vllm_client.py) referenced from [vLLM official implementation - client](https://github.com/vllm-project/vllm/blob/main/examples/api_client.py).

