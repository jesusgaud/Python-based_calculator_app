import os
import qrcode
from datetime import datetime

# Get environment variables with defaults
qr_data = os.getenv('QR_DATA_URL', 'https://github.com/jesusgaud')
qr_dir = os.getenv('QR_CODE_DIR', 'qr_codes')
filename = os.getenv('QR_CODE_FILENAME', f'qr_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
fill_color = os.getenv('FILL_COLOR', 'black')
back_color = os.getenv('BACK_COLOR', 'white')

# Ensure the output directory exists
output_path = os.path.join(os.getcwd(), qr_dir)
os.makedirs(output_path, exist_ok=True)

# Create QR code object
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data(qr_data)
qr.make(fit=True)

# Generate QR image with custom colors
img = qr.make_image(fill_color=fill_color, back_color=back_color)

# Save the image
img_path = os.path.join(output_path, filename)
img.save(img_path)

# Print confirmation
print(f"QR code generated at: {img_path}")
print(f"🔗 URL encoded: {qr_data}")
