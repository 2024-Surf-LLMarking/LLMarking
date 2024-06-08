from vllm import AsyncEngineArgs,AsyncLLMEngine
from vllm.inputs import TokensPrompt
from vllm.sampling_params import SamplingParams
from transformers import AutoTokenizer, GenerationConfig
from huggingface_hub import snapshot_download
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
import uvicorn
from prompt_utils import remove_stop_words, _build_prompt_self
import uuid
import json 
import argparse

# http接口服务
app=FastAPI()


__all__ = ["Qwen/Qwen1.5-14B-Chat-GPTQ-Int4", 
           "Qwen/Qwen1.5-32B-Chat-AWQ", 
           "internlm/internlm2-chat-7b", 
           "01-ai/Yi-1.5-9B-Chat",
           "modelscope/Yi-1.5-34B-Chat-AWQ",
           "CohereForAI/aya-23-8B",
           "meta-llama/Meta-Llama-3-8B-Instruct",
           "THUDM/glm-4-9b-chat",
           "Qwen/Qwen2-7B-Instruct",
           "google/gemma-1.1-7b-it",
           "mistralai/Mistral-7B-Instruct-v0.3",
           "microsoft/Phi-3-small-8k-instruct",
           "openbmb/MiniCPM-2B-dpo-bf16-llama-format"
           ]

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--model", type=int, default=0)
arg = parser.parse_args()

# vLLM参数
model_dir=__all__[arg.model]
tensor_parallel_size=1
gpu_memory_utilization=0.95
if model_dir == __all__[0]:
    quantization = 'gptq'
elif model_dir == __all__[1] or model_dir == __all__[4]:
    quantization = 'awq'
else:
    quantization = None
dtype='float16'

if model_dir not in __all__:
    raise NotImplementedError(f'Model selected: [{model_dir}], has not been implemented by this project!')

# vLLM模型加载
def load_vllm():
    global generation_config,tokenizer,stop_words_ids,engine    
    # 模型下载
    snapshot_download(model_dir)
    # 模型基础配置
    generation_config=GenerationConfig.from_pretrained(model_dir,trust_remote_code=True)
    # 加载分词器
    tokenizer=AutoTokenizer.from_pretrained(model_dir,trust_remote_code=True)
    if model_dir == __all__[7] or model_dir == __all__[6] or model_dir == __all__[9] or model_dir == __all__[11]:
        pass
    else:
        tokenizer.eos_token_id=generation_config.eos_token_id
    # 推理终止词
    
    
    if model_dir in __all__[:2] or model_dir == __all__[8]:
        tokenizer.im_start_id = 151644
        tokenizer.im_end_id = 151645
        generation_config.max_window_size = 11000
    elif model_dir == __all__[2]:
        tokenizer.im_start_id = 92542
        tokenizer.im_end_id = 92543
        generation_config.max_window_size = 31648
    elif model_dir == __all__[3] or model_dir == __all__[4]:
        tokenizer.im_start_id = 1
        tokenizer.im_end_id = 7
        generation_config.max_window_size = 4096
    elif model_dir == __all__[5] or model_dir == __all__[6] or model_dir == __all__[9] or model_dir == __all__[11]:
        tokenizer.im_start_id = None
        tokenizer.im_end_id = None
        generation_config.max_window_size = 8192
    elif model_dir == __all__[7] or model_dir == __all__[10] or model_dir == __all__[12]:
        tokenizer.im_start_id = None
        tokenizer.im_end_id = None
        generation_config.max_window_size = 11000

    if model_dir == __all__[7]:
        stop_words_ids = [tokenizer.eos_token_id, 151336]
    elif model_dir == __all__[11]:
        stop_words_ids = [tokenizer.eos_token_id, 100266]
    else:
        stop_words_ids = [tokenizer.im_start_id, tokenizer.im_end_id, tokenizer.eos_token_id]

    # vLLM基础配置
    args=AsyncEngineArgs(model_dir)
    args.worker_use_ray=False
    args.engine_use_ray=False
    args.tokenizer=model_dir
    args.tensor_parallel_size=tensor_parallel_size
    args.trust_remote_code=True
    args.quantization=quantization
    args.gpu_memory_utilization=gpu_memory_utilization
    args.dtype=dtype
    args.max_num_seqs=20    # batch最大20条样本
    args.max_model_len=generation_config.max_window_size if model_dir != __all__[1] else 3024
    # 加载模型
    # os.environ['VLLM_USE_MODELSCOPE']='True'
    engine=AsyncLLMEngine.from_engine_args(args)
    return generation_config,tokenizer,stop_words_ids,engine

generation_config,tokenizer,stop_words_ids,engine=load_vllm()

# 用户停止句匹配
def match_user_stop_words(response_token_ids,user_stop_tokens):
    for stop_tokens in user_stop_tokens:
        if len(response_token_ids)<len(stop_tokens):
            continue 
        if response_token_ids[-len(stop_tokens):]==stop_tokens:
            return True  # 命中停止句, 返回True
    return False

# chat对话接口
@app.post("/chat")
async def chat(request: Request):
    request=await request.json()
    
    query=request.get('query',None)
    history=request.get('history',[])
    system=request.get('system','You are a helpful assistant.') if model_dir != __all__[6] and model_dir != __all__[9] and model_dir != __all__[10] else None
    stream=request.get("stream",False)
    user_stop_words=request.get("user_stop_words",[])    # list[str]，用户自定义停止句，例如：['Observation: ', 'Action: ']定义了2个停止句，遇到任何一个都会停止
    
    if query is None:
        return Response(status_code=502,content='query is empty')

    # 用户停止词
    user_stop_tokens=[]
    for words in user_stop_words:
        user_stop_tokens.append(tokenizer.encode(words))
    
    # 构造prompt
    # prompt_text,prompt_tokens=_build_prompt(generation_config,tokenizer,query,history=history,system=system)

    prompt_tokens=_build_prompt_self(generation_config,tokenizer,query,history=history,system=system)
        
    # vLLM请求配置
    sampling_params=SamplingParams(stop_token_ids=stop_words_ids, 
                                    early_stopping=False,
                                    top_p=generation_config.top_p,
                                    top_k=-1 if generation_config.top_k == 0 else generation_config.top_k,
                                    temperature=generation_config.temperature,
                                    repetition_penalty=generation_config.repetition_penalty,
                                    max_tokens=generation_config.max_new_tokens
                                   )
    # vLLM异步推理（在独立线程中阻塞执行推理，主线程异步等待完成通知）
    request_id=str(uuid.uuid4().hex)
    results_iter=engine.generate(sampling_params=sampling_params,inputs=TokensPrompt(prompt_token_ids=prompt_tokens),request_id=request_id)
    
    # 流式返回，即迭代transformer的每一步推理结果并反复返回
    if stream:
        async def streaming_resp():
            async for result in results_iter:
                # 移除im_end,eos等系统停止词
                token_ids=remove_stop_words(result.outputs[0].token_ids,stop_words_ids)
                # 返回截止目前的tokens输出                
                text=tokenizer.decode(token_ids)
                yield (json.dumps({'text':text})+'\0').encode('utf-8')
                # 匹配用户停止词,终止推理
                if match_user_stop_words(token_ids,user_stop_tokens):
                    await engine.abort(request_id)   # 终止vllm后续推理
                    break
        return StreamingResponse(streaming_resp())

    # 整体一次性返回模式
    async for result in results_iter:
        # 移除im_end,eos等系统停止词
        token_ids=remove_stop_words(result.outputs[0].token_ids,stop_words_ids)
        # 返回截止目前的tokens输出                
        text=tokenizer.decode(token_ids)
        # 匹配用户停止词,终止推理
        if match_user_stop_words(token_ids,user_stop_tokens):
            await engine.abort(request_id)   # 终止vllm后续推理
            break

    ret={"text":text}
    return JSONResponse(ret)

if __name__=='__main__':
    uvicorn.run(app,
                host=None,
                port=8000,
                log_level="debug")
