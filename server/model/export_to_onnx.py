import torch
import torch.nn as nn

# --- Визначення моделі U-Net (спрощена версія) ---
class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.enc1 = nn.Sequential(nn.Conv2d(3, 64, 3, padding=1), nn.ReLU())
        self.enc2 = nn.Sequential(nn.Conv2d(64, 128, 3, padding=1), nn.ReLU())
        self.dec1 = nn.Sequential(nn.Conv2d(128, 64, 3, padding=1), nn.ReLU())
        self.out = nn.Conv2d(64, 3, 1)

    def forward(self, x):
        x1 = self.enc1(x)
        x2 = self.enc2(x1)
        x3 = self.dec1(x2)
        return self.out(x3)

# --- Ініціалізація моделі ---
model = UNet()
# Якщо є навчені ваги, завантаж їх:
# model.load_state_dict(torch.load("server/model/weights/unet64.pth", map_location="cpu"))

model.eval()

# --- Приклад вхідного тензора ---
dummy_input = torch.randn(1, 3, 64, 64)

# --- Експорт у ONNX ---
torch.onnx.export(
    model,
    dummy_input,
    "unet64.onnx",
    opset_version=18,           # сучасний opset
    export_params=True,         # включає ваги у сам файл .onnx
    do_constant_folding=True,   # оптимізація
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)

print("✅ Exported to unet64.onnx")
