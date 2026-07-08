import torch
from unet.unet_model import UNet   # використовуємо повний UNet з репозиторію

# --- Ініціалізація моделі ---
model = UNet(n_channels=3, n_classes=2, bilinear=False)

# --- Завантаження навчених ваг ---
model.load_state_dict(torch.load("server/model/weights/unet64.pth", map_location="cpu"))
model.eval()

# --- Приклад вхідного тензора ---
dummy_input = torch.randn(1, 3, 512, 512)   # розмір має збігатися з тим, на якому тренувалася модель

# --- Експорт у ONNX ---
torch.onnx.export(
    model,
    dummy_input,
    "server/model/unet64.onnx",
    opset_version=18,
    export_params=True,         # включає ваги у файл
    do_constant_folding=True,   # оптимізація
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

print("✅ Exported to server/model/unet64.onnx")
