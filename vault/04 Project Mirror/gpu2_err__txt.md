---
argos_import: project_file
source_path: gpu2_err.txt
source_abs: F:\debug\argoss\gpu2_err.txt
source_ext: .txt
source_sha256: ed1145a57dd68cc9d06fd2ce7fbd3223d1e8de770917c1c35967fb6cd64e81f5
text_sha256: 0f966870fd6f13cd7c1b8c3762c829fa406b7525544d4f3da331c1dddc974e57
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-05 01:32:44
---

# gpu2_err.txt

- Source: `gpu2_err.txt`
- Extract: `text`
- SHA256: `ed1145a57dd68cc9d06fd2ce7fbd3223d1e8de770917c1c35967fb6cd64e81f5`

## Content

load_backend: loaded Vulkan backend from C:\Users\AvA\.docker\bin\inference\ggml-vulkan.dll
load_backend: loaded CPU backend from C:\Users\AvA\.docker\bin\inference\ggml-cpu-haswell.dll
main: n_parallel is set to auto, using n_parallel = 4 and kv_unified = true
build_info: b1-e365e65
system_info: n_threads = 4 (n_threads_batch = 4) / 8 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | LLAMAFILE = 1 | REPACK = 1 | 
init: using 8 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model 'F:\ROCm\models\phi4-mini.gguf'
common_init_result: fitting params to device memory, for bugs during this step try to reproduce them with -fit off, or provide --verbose logs if the bug only occurs with -fit on
llama_params_fit_impl: projected memory use with initial parameters [MiB]:
llama_params_fit_impl:   - Vulkan0 (Radeon RX 580 Series):   4096 total,   1237 used,   1932 free vs. target of   1024
llama_params_fit_impl:   - Vulkan1 (Radeon RX 560 Series):   4096 total,   1947 used,   1222 free vs. target of   1024
llama_params_fit_impl: projected to use 3185 MiB of device memory vs. 6339 MiB of free device memory
llama_params_fit_impl: targets for free memory can be met on all devices, no changes needed
llama_params_fit: successfully fit params to free device memory
llama_params_fit: fitting params to free memory took 2.07 seconds
llama_model_load_from_file_impl: using device Vulkan0 (Radeon RX 580 Series) (unknown id) - 3169 MiB free
llama_model_load_from_file_impl: using device Vulkan1 (Radeon RX 560 Series) (unknown id) - 3169 MiB free
llama_model_loader: loaded meta data with 36 key-value pairs and 196 tensors from F:\ROCm\models\phi4-mini.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = phi3
llama_model_loader: - kv   1:              phi3.rope.scaling.attn_factor f32              = 1.190238
llama_model_loader: - kv   2:                               general.type str              = model
llama_model_loader: - kv   3:                               general.name str              = Phi 4 Mini Instruct
llama_model_loader: - kv   4:                           general.finetune str              = instruct
llama_model_loader: - kv   5:                           general.basename str              = Phi-4
llama_model_loader: - kv   6:                         general.size_label str              = mini
llama_model_loader: - kv   7:                            general.license str              = mit
llama_model_loader: - kv   8:                       general.license.link str              = https://huggingface.co/microsoft/Phi-...
llama_model_loader: - kv   9:                               general.tags arr[str,3]       = ["nlp", "code", "text-generation"]
llama_model_loader: - kv  10:                          general.languages arr[str,24]      = ["multilingual", "ar", "zh", "cs", "d...
llama_model_loader: - kv  11:                        phi3.context_length u32              = 131072
llama_model_loader: - kv  12:  phi3.rope.scaling.original_context_length u32              = 4096
llama_model_loader: - kv  13:                      phi3.embedding_length u32              = 3072
llama_model_loader: - kv  14:                   phi3.feed_forward_length u32              = 8192
llama_model_loader: - kv  15:                           phi3.block_count u32              = 32
llama_model_loader: - kv  16:                  phi3.attention.head_count u32              = 24
llama_model_loader: - kv  17:               phi3.attention.head_count_kv u32              = 8
llama_model_loader: - kv  18:      phi3.attention.layer_norm_rms_epsilon f32              = 0.000010
llama_model_loader: - kv  19:                  phi3.rope.dimension_count u32              = 96
llama_model_loader: - kv  20:                        phi3.rope.freq_base f32              = 10000.000000
llama_model_loader: - kv  21:              phi3.attention.sliding_window u32              = 262144
llama_model_loader: - kv  22:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  23:                         tokenizer.ggml.pre str              = gpt-4o
llama_model_loader: - kv  24:                      tokenizer.ggml.tokens arr[str,200064]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  25:                  tokenizer.ggml.token_type arr[i32,200064]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  26:                      tokenizer.ggml.merges arr[str,199742]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "e r", ...
llama_model_loader: - kv  27:                tokenizer.ggml.bos_token_id u32              = 199999
llama_model_loader: - kv  28:                tokenizer.ggml.eos_token_id u32              = 199999
llama_model_loader: - kv  29:            tokenizer.ggml.unknown_token_id u32              = 199999
llama_model_loader: - kv  30:            tokenizer.ggml.padding_token_id u32              = 199999
llama_model_loader: - kv  31:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  32:               tokenizer.ggml.add_eos_token bool             = false
llama_model_loader: - kv  33:                    tokenizer.chat_template str              = {% for message in messages %}{% if me...
llama_model_loader: - kv  34:               general.quantization_version u32              = 2
llama_model_loader: - kv  35:                          general.file_type u32              = 15
llama_model_loader: - type  f32:   67 tensors
llama_model_loader: - type q4_K:   80 tensors
llama_model_loader: - type q5_K:   32 tensors
llama_model_loader: - type q6_K:   17 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_K - Medium
print_info: file size   = 2.31 GiB (5.18 BPW) 
load_hparams: Phi SWA is currently disabled - results might be suboptimal for some models (see https://github.com/ggml-org/llama.cpp/pull/13676)
load: 0 unused tokens
load: printing all EOG tokens:
load:   - 199999 ('<|endoftext|>')
load:   - 200020 ('<|end|>')
load: special tokens cache size = 12
load: token to piece cache size = 1.3333 MB
print_info: arch                  = phi3
print_info: vocab_only            = 0
print_info: no_alloc              = 0
print_info: n_ctx_train           = 131072
print_info: n_embd                = 3072
print_info: n_embd_inp            = 3072
print_info: n_layer               = 32
print_info: n_head                = 24
print_info: n_head_kv             = 8
print_info: n_rot                 = 96
print_info: n_swa                 = 0
print_info: is_swa_any            = 0
print_info: n_embd_head_k         = 128
print_info: n_embd_head_v         = 128
print_info: n_gqa                 = 3
print_info: n_embd_k_gqa          = 1024
print_info: n_embd_v_gqa          = 1024
print_info: f_norm_eps            = 0.0e+00
print_info: f_norm_rms_eps        = 1.0e-05
print_info: f_clamp_kqv           = 0.0e+00
print_info: f_max_alibi_bias      = 0.0e+00
print_info: f_logit_scale         = 0.0e+00
print_info: f_attn_scale          = 0.0e+00
print_info: n_ff                  = 8192
print_info: n_expert              = 0
print_info: n_expert_used         = 0
print_info: n_expert_groups       = 0
print_info: n_group_used          = 0
print_info: causal attn           = 1
print_info: pooling type          = -1
print_info: rope type             = 2
print_info: rope scaling          = linear
print_info: freq_base_train       = 10000.0
print_info: freq_scale_train      = 1
print_info: n_ctx_orig_yarn       = 4096
print_info: rope_yarn_log_mul     = 0.0000
print_info: rope_finetuned        = unknown
print_info: model type            = 3B
print_info: model params          = 3.84 B
print_info: general.name          = Phi 4 Mini Instruct
print_info: vocab type            = BPE
print_info: n_vocab               = 200064
print_info: n_merges              = 199742
print_info: BOS token             = 199999 '<|endoftext|>'
print_info: EOS token             = 199999 '<|endoftext|>'
print_info: EOT token             = 199999 '<|endoftext|>'
print_info: UNK token             = 199999 '<|endoftext|>'
print_info: PAD token             = 199999 '<|endoftext|>'
print_info: LF token              = 198 'Ċ'
print_info: EOG token             = 199999 '<|endoftext|>'
print_info: EOG token             = 200020 '<|end|>'
print_info: max token length      = 256
load_tensors: loading model tensors, this can take a while... (mmap = true, direct_io = false)
load_tensors: offloading output layer to GPU
load_tensors: offloading 31 repeating layers to GPU
load_tensors: offloaded 33/33 layers to GPU
load_tensors:   CPU_Mapped model buffer size =   480.81 MiB
load_tensors:      Vulkan0 model buffer size =   999.77 MiB
load_tensors:      Vulkan1 model buffer size =  1368.79 MiB
.....................................................................
common_init_result: added <|endoftext|> logit bias = -inf
common_init_result: added <|end|> logit bias = -inf
llama_context: constructing llama_context
llama_context: n_seq_max     = 4
llama_context: n_ctx         = 2048
llama_context: n_ctx_seq     = 2048
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = auto
llama_context: kv_unified    = true
llama_context: freq_base     = 10000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_seq (2048) < n_ctx_train (131072) -- the full capacity of the model will not be utilized
llama_context: Vulkan_Host  output buffer size =     3.05 MiB
llama_kv_cache:    Vulkan0 KV buffer size =   136.00 MiB
llama_kv_cache:    Vulkan1 KV buffer size =   120.00 MiB
llama_kv_cache: size =  256.00 MiB (  2048 cells,  32 layers,  4/1 seqs), K (f16):  128.00 MiB, V (f16):  128.00 MiB
llama_kv_cache: attn_rot_k = 0, n_embd_head_k_all = 128
llama_kv_cache: attn_rot_v = 0, n_embd_head_k_all = 128
llama_context: pipeline parallelism enabled
sched_reserve: reserving ...
sched_reserve: Flash Attention was auto, set to enabled
sched_reserve: resolving fused Gated Delta Net support:
sched_reserve: fused Gated Delta Net (autoregressive) enabled
sched_reserve: fused Gated Delta Net (chunked) enabled
ggml_vulkan: Device memory allocation of size 455917568 failed.
ggml_vulkan: vk::Device::allocateMemory: ErrorOutOfDeviceMemory
ggml_gallocr_reserve_n_impl: failed to allocate Vulkan1 buffer of size 455917568
graph_reserve: failed to allocate compute buffers
sched_reserve: compute buffer allocation failed, retrying without pipeline parallelism
ggml_vulkan: Device memory allocation of size 416022528 failed.
ggml_vulkan: vk::Device::allocateMemory: ErrorOutOfDeviceMemory
ggml_gallocr_reserve_n_impl: failed to allocate Vulkan1 buffer of size 416022528
graph_reserve: failed to allocate compute buffers

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
