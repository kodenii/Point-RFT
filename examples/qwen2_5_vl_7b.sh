source activate RL

export VLLM_ATTENTION_BACKEND=XFORMERS
export VLLM_USE_V1=0

export WANDB_API_KEY=
export DEBUG_MODE="true"
export WANDB_ENTITY=
export WANDB_RESUME=never  # Set in terminal
unset WANDB_RUN_ID
export WANDB_PROJECT=EasyR1

MODEL_PATH= # replace it with your local file path

SYSTEM_PROMPT="Output the thinking process in <think> </think> with related point(s) in XML format and final answer (one word) in <answer> </answer> tags."

python3 -m verl.trainer.main \
    config=examples/config.yaml \
    data.train_files=HuggingFaceM4/ChartQA@train \
    data.val_files=HuggingFaceM4/ChartQA@test \
    data.prompt_key=query \
    data.answer_key=label \
    data.image_key=image \
    data.system_prompt="${SYSTEM_PROMPT}" \
    worker.actor.model.model_path=${MODEL_PATH} \
    worker.rollout.tensor_parallel_size=1 \
    worker.rollout.enable_chunked_prefill=false \
    trainer.experiment_name=qwen2_5_vl_3b_chartqa \
    trainer.n_gpus_per_node=8 \
    trainer.save_checkpoint_path=
