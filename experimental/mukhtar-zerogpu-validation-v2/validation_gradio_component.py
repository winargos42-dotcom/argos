"""Add a separate safe v2 validation panel inside existing app.py Gradio Blocks.

Integration: inside the existing with gr.Blocks(...) as demo: block add:
    from validation_gradio_component import mount_validation_panel
    mount_validation_panel()

Do not remove the old v1 UI; this is additive. CPU-only quota guard runs
first. A GPU allocation is requested only after that check succeeds.
"""
import gradio as gr
import spaces
from validation_search import run_from_pinned_assets


def approve_validation_run(quota_confirmed):
    if quota_confirmed is not True:
        raise gr.Error(
            "Перед запуском проверьте оставшуюся бесплатную квоту ZeroGPU. "
            "Без подтверждения GPU не запрашивается."
        )
    return True


@spaces.GPU(duration=40)
def run_validation_on_gpu(quota_confirmed):
    if quota_confirmed is not True:
        raise gr.Error("ZeroGPU не выделена: отсутствует подтверждение квоты")
    try:
        metrics, checkpoint, report = run_from_pinned_assets(require_cuda=True)
    except Exception as exc:
        # Avoid disclosing local GPU paths/credentials in a public Space.
        raise gr.Error("Validation experiment failed: " + type(exc).__name__) from None
    message = (
        f"✅ CUDA: **{metrics['gpu_name']}**. Проверено "
        f"**{len(metrics['candidates'])} комбинаций**; "
        f"валидация **{metrics['baseline_val_mae']:.6f} → "
        f"{metrics['best']['val_mae']:.6f}**. "
        f"Финальный MAE на 128 состояниях: {metrics['final_heldout_mae']:.6f}. "
        "Это контроль дообучения компактной MLP, не весь MaleCNS."
    )
    return message, metrics, checkpoint, report


def mount_validation_panel():
    """Call only inside an existing Gradio Blocks context."""
    with gr.Accordion("🔬 Validation v2: 3 seeds × 2 LR, early stopping", open=False):
        gr.Markdown(
            "Новый научный режим: фиксированный stratified split 288 train / 72 val; "
            "шесть комбинаций (7,21,42) × (0.0001,0.0003), максимум "
            "80 шагов на вариант. Выбор делается только по validation MAE. "
            "128 прежних holdout-состояний оцениваются **после выбора**, один раз. "
            "Ранее они уже использовались, поэтому это не новая независимая оценка."
        )
        gr.Markdown(
            "**Оплата:** ZeroGPU имеет ограниченную бесплатную квоту. "
            "После её окончания HF PRO может расходовать предоплаченные кредиты. "
            "Проверьте остаток до каждого вызова; это не автоматический контроль биллинга."
        )
        confirmed = gr.Checkbox(
            label="Я проверил оставшуюся бесплатную ZeroGPU-квоту; разрешаю ровно один 40-секундный вызов",
            value=False,
        )
        button = gr.Button("Запустить один ZeroGPU validation-v2 experiment")
        message = gr.Markdown("Не запущено.")
        metrics = gr.JSON(label="Поиск, валидация, итоговый тест (без отбора по тесту)")
        checkpoint = gr.File(label="Selected checkpoint, safetensors")
        report = gr.File(label="Полный JSON-отчёт")
        gate = gr.State(False)
        button.click(
            approve_validation_run, inputs=[confirmed], outputs=[gate], queue=False,
            api_name=False,
        ).success(
            run_validation_on_gpu, inputs=[gate],
            outputs=[message, metrics, checkpoint, report],
            concurrency_limit=1, api_name=False,
        )
