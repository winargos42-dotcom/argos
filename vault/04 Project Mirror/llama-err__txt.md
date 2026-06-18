---
argos_import: project_file
source_path: llama-err.txt
source_abs: F:\debug\argoss\llama-err.txt
source_ext: .txt
source_sha256: c1602fa4b28a57d3724aec585ceab57b853a5d4baf3e5ed56a4960397f40a78a
text_sha256: a7d335a2324cb64d5cdb76097203b211b68013f13542453de7888e9c027c42af
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:12:02
---

# llama-err.txt

- Source: `llama-err.txt`
- Extract: `text`
- SHA256: `c1602fa4b28a57d3724aec585ceab57b853a5d4baf3e5ed56a4960397f40a78a`

## Content

load_backend: loaded Vulkan backend from C:\Users\AvA\.docker\bin\inference\ggml-vulkan.dll
load_backend: loaded CPU backend from C:\Users\AvA\.docker\bin\inference\ggml-cpu-haswell.dll
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build_info: b1-e365e65
system_info: n_threads = 4 (n_threads_batch = 4) / 8 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | LLAMAFILE = 1 | REPACK = 1 | 
init: using 8 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model 'F:\ROCm\models\DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf'
common_init_result: fitting params to device memory, for bugs during this step try to reproduce them with -fit off, or provide --verbose logs if the bug only occurs with -fit on
llama_params_fit_impl: projected memory use with initial parameters [MiB]:
llama_params_fit_impl:   - Vulkan0 (Radeon RX 560 Series):   4096 total,   3920 used,   -750 free vs. target of   1024
llama_params_fit_impl:   - Vulkan1 (Radeon RX 580 Series):   4096 total,   3783 used,   -613 free vs. target of   1024
llama_params_fit_impl: projected to use 7704 MiB of device memory vs. 6339 MiB of free device memory
llama_params_fit_impl: cannot meet free memory targets on all devices, need to use 3412 MiB less in total
llama_params_fit_impl: context size set by user to 512 -> no change
llama_params_fit: failed to fit params to free device memory: n_gpu_layers already set by user to 20, abort
llama_params_fit: fitting params to free memory took 2.04 seconds
llama_model_load_from_file_impl: using device Vulkan0 (Radeon RX 560 Series) (unknown id) - 3169 MiB free
llama_model_load_from_file_impl: using device Vulkan1 (Radeon RX 580 Series) (unknown id) - 3169 MiB free
llama_model_loader: loaded meta data with 42 key-value pairs and 377 tensors from F:\ROCm\models\DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = deepseek2
llama_model_loader: - kv   1:                               general.name str              = DeepSeek-Coder-V2-Lite-Instruct
llama_model_loader: - kv   2:                      deepseek2.block_count u32              = 27
llama_model_loader: - kv   3:                   deepseek2.context_length u32              = 163840
llama_model_loader: - kv   4:                 deepseek2.embedding_length u32              = 2048
llama_model_loader: - kv   5:              deepseek2.feed_forward_length u32              = 10944
llama_model_loader: - kv   6:             deepseek2.attention.head_count u32              = 16
llama_model_loader: - kv   7:          deepseek2.attention.head_count_kv u32              = 16
llama_model_loader: - kv   8:                   deepseek2.rope.freq_base f32              = 10000.000000
llama_model_loader: - kv   9: deepseek2.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  10:                deepseek2.expert_used_count u32              = 6
llama_model_loader: - kv  11:                          general.file_type u32              = 15
llama_model_loader: - kv  12:        deepseek2.leading_dense_block_count u32              = 1
llama_model_loader: - kv  13:                       deepseek2.vocab_size u32              = 102400
llama_model_loader: - kv  14:           deepseek2.attention.kv_lora_rank u32              = 512
llama_model_loader: - kv  15:             deepseek2.attention.key_length u32              = 192
llama_model_loader: - kv  16:           deepseek2.attention.value_length u32              = 128
llama_model_loader: - kv  17:       deepseek2.expert_feed_forward_length u32              = 1408
llama_model_loader: - kv  18:                     deepseek2.expert_count u32              = 64
llama_model_loader: - kv  19:              deepseek2.expert_shared_count u32              = 2
llama_model_loader: - kv  20:             deepseek2.expert_weights_scale f32              = 1.000000
llama_model_loader: - kv  21:             deepseek2.rope.dimension_count u32              = 64
llama_model_loader: - kv  22:                deepseek2.rope.scaling.type str              = yarn
llama_model_loader: - kv  23:              deepseek2.rope.scaling.factor f32              = 40.000000
llama_model_loader: - kv  24: deepseek2.rope.scaling.original_context_length u32              = 4096
llama_model_loader: - kv  25: deepseek2.rope.scaling.yarn_log_multiplier f32              = 0.070700
llama_model_loader: - kv  26:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  27:                         tokenizer.ggml.pre str              = deepseek-llm
llama_model_loader: - kv  28:                      tokenizer.ggml.tokens arr[str,102400]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  29:                  tokenizer.ggml.token_type arr[i32,102400]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  30:                      tokenizer.ggml.merges arr[str,99757]   = ["Ġ Ġ", "Ġ t", "Ġ a", "i n", "h e...
llama_model_loader: - kv  31:                tokenizer.ggml.bos_token_id u32              = 100000
llama_model_loader: - kv  32:                tokenizer.ggml.eos_token_id u32              = 100001
llama_model_loader: - kv  33:            tokenizer.ggml.padding_token_id u32              = 100001
llama_model_loader: - kv  34:               tokenizer.ggml.add_bos_token bool             = true
llama_model_loader: - kv  35:               tokenizer.ggml.add_eos_token bool             = false
llama_model_loader: - kv  36:                    tokenizer.chat_template str              = {% if not add_generation_prompt is de...
llama_model_loader: - kv  37:               general.quantization_version u32              = 2
llama_model_loader: - kv  38:                      quantize.imatrix.file str              = /models/DeepSeek-Coder-V2-Lite-Instru...
llama_model_loader: - kv  39:                   quantize.imatrix.dataset str              = /training_data/calibration_datav3.txt
llama_model_loader: - kv  40:             quantize.imatrix.entries_count i32              = 293
llama_model_loader: - kv  41:              quantize.imatrix.chunks_count i32              = 139
llama_model_loader: - type  f32:  108 tensors
llama_model_loader: - type q5_0:   14 tensors
llama_model_loader: - type q8_0:   13 tensors
llama_model_loader: - type q4_K:  229 tensors
llama_model_loader: - type q6_K:   13 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_K - Medium
print_info: file size   = 9.65 GiB (5.28 BPW) 
load: control-looking token: 100004 '<｜fim▁end｜>' was not control-type; this is probably a bug in the model. its type will be overridden
load: control-looking token: 100002 '<｜fim▁hole｜>' was not control-type; this is probably a bug in the model. its type will be overridden
load: control-looking token: 100003 '<｜fim▁begin｜>' was not control-type; this is probably a bug in the model. its type will be overridden
load: 0 unused tokens
load: printing all EOG tokens:
load:   - 100001 ('<｜end▁of▁sentence｜>')
load: special tokens cache size = 2400
load: token to piece cache size = 0.6661 MB
print_info: arch                  = deepseek2
print_info: vocab_only            = 0
print_info: no_alloc              = 0
print_info: n_ctx_train           = 163840
print_info: n_embd                = 2048
print_info: n_embd_inp            = 2048
print_info: n_layer               = 27
print_info: n_head                = 16
print_info: n_head_kv             = 16
print_info: n_rot                 = 64
print_info: n_swa                 = 0
print_info: is_swa_any            = 0
print_info: n_embd_head_k         = 192
print_info: n_embd_head_v         = 128
print_info: n_gqa                 = 1
print_info: n_embd_k_gqa          = 3072
print_info: n_embd_v_gqa          = 2048
print_info: f_norm_eps            = 0.0e+00
print_info: f_norm_rms_eps        = 1.0e-06
print_info: f_clamp_kqv           = 0.0e+00
print_info: f_max_alibi_bias      = 0.0e+00
print_info: f_logit_scale         = 0.0e+00
print_info: f_attn_scale          = 0.0e+00
print_info: n_ff                  = 10944
print_info: n_expert              = 64
print_info: n_expert_used         = 6
print_info: n_expert_groups       = 0
print_info: n_group_used          = 0
print_info: causal attn           = 1
print_info: pooling type          = -1
print_info: rope type             = 0
print_info: rope scaling          = yarn
print_info: freq_base_train       = 10000.0
print_info: freq_scale_train      = 0.025
print_info: n_ctx_orig_yarn       = 4096
print_info: rope_yarn_log_mul     = 0.7070
print_info: rope_finetuned        = unknown
print_info: model type            = 16B
print_info: model params          = 15.71 B
print_info: general.name          = DeepSeek-Coder-V2-Lite-Instruct
print_info: n_layer_dense_lead    = 1
print_info: n_lora_q              = 0
print_info: n_lora_kv             = 512
print_info: n_embd_head_k_mla     = 192
print_info: n_embd_head_v_mla     = 128
print_info: n_ff_exp              = 1408
print_info: n_expert_shared       = 2
print_info: expert_weights_scale  = 1.0
print_info: expert_weights_norm   = 0
print_info: expert_gating_func    = softmax
print_info: vocab type            = BPE
print_info: n_vocab               = 102400
print_info: n_merges              = 99757
print_info: BOS token             = 100000 '<｜begin▁of▁sentence｜>'
print_info: EOS token             = 100001 '<｜end▁of▁sentence｜>'
print_info: EOT token             = 100001 '<｜end▁of▁sentence｜>'
print_info: PAD token             = 100001 '<｜end▁of▁sentence｜>'
print_info: LF token              = 185 'Ċ'
print_info: FIM PRE token         = 100003 '<｜fim▁begin｜>'
print_info: FIM SUF token         = 100002 '<｜fim▁hole｜>'
print_info: FIM MID token         = 100004 '<｜fim▁end｜>'
print_info: EOG token             = 100001 '<｜end▁of▁sentence｜>'
print_info: max token length      = 256
load_tensors: loading model tensors, this can take a while... (mmap = true, direct_io = false)
ggml_vulkan: Device memory allocation of size 767432704 failed.
ggml_vulkan: vk::Device::allocateMemory: ErrorOutOfDeviceMemory
alloc_tensor_range: failed to allocate Vulkan0 buffer of size 767432704
llama_model_load: error loading model: unable to allocate Vulkan0 buffer
llama_model_load_from_file_impl: failed to load model
common_init_from_params: failed to load model 'F:\ROCm\models\DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf'
srv    load_model: failed to load model, 'F:\ROCm\models\DeepSeek-Coder-V2-Lite-Instruct-Q4_K_M.gguf'
srv    operator(): operator(): cleaning up before exit...

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
