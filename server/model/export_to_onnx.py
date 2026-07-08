import torch
import torch.nn as nn

# --- Your U-Net model definition ---
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

# --- Load your trained weights if you have them ---
model = UNet()
# model.load_state_dict(torch.load("model.pth", map_location="cpu"))

model.eval()

dummy_input = torch.randn(1, 3, 64, 64)

torch.onnx.export(
    model,
    dummy_input,
    "unet64.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=18
)

print("Exported to unet64.onnx")
