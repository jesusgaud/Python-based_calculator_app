# 📦 QR Code Generator with Docker + Python

This mini project demonstrates how to generate a **QR code PNG** using a Python script inside a **Docker container**. When scanned, the QR code redirects users to your GitHub profile.

---

## 🔧 Features

- Accepts environment variables for full QR code customization
- Generates a PNG image with a link to your GitHub profile
- Supports color and filename configuration
- Dockerized for portability and ease of deployment

---

## 🚀 Getting Started

### 📁 Project Structure


---

### 🐳 Build the Docker Image
```sh
From the `qr-code-docker/` directory:
```

```sh
sudo docker build -t my-qr-app .

```
### Run the Container
```sh

> Replace `YOUR_GITHUB_USERNAME` and the volume mount path with your own values.
sudo docker run -d --name qr-generator \
  -e QR_DATA_URL='https://github.com/YOUR_GITHUB_USERNAME' \
  -e QR_CODE_DIR='qr_codes' \
  -e QR_CODE_FILENAME='mygithubQR.png' \
  -e FILL_COLOR='black' \
  -e BACK_COLOR='white' \
  -v "/absolute/path/to/your/project/qr-code-docker/app/qr_codes:/app/qr_codes" \
  my-qr-app
```
### 📄 Container Logs

```sh
sudo docker logs qr-generator
```

### 🧹 Helpful Docker Commands

| Command      | Description                 |
|-------------|-----------------------------|
| `docker ps`	| List running containers |
| `docker logs` | qr-generator	View container logs |
| `docker stop qr-generator`	| Stop the container |
| `docker rm qr-generator`	| Remove the container |
| `docker images`	| List Docker images |
| `docker rmi my-qr-app`	| Delete the image|

## 📜 License

This project is licensed under the **MIT License**.

---

## 📞 Contact

For questions, please reach out via **[GitHub Issues](https://github.com/jesusgaud/Python-based_calculator_app/issues)**.
