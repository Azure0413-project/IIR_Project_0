export MODEL_NAME="runwayml/stable-diffusion-v1-5"
export INSTANCE_DIR="beaf"
export OUTPUT_DIR="beaf-model"

#huggingface-cli login

accelerate launch train_dreambooth_lora.py \
  --pretrained_model_name_or_path=$MODEL_NAME  \
  --instance_data_dir=$INSTANCE_DIR \
  --output_dir=$OUTPUT_DIR \
  --instance_prompt="a photo of steak or beaf" \
  --resolution=512 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=1 \
  --checkpointing_steps=100 \
  --learning_rate=1e-4 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --max_train_steps=10 \
  --validation_prompt="a photo of steak" \
  --validation_epochs=50 \
  --seed="0" \
  --push_to_hub