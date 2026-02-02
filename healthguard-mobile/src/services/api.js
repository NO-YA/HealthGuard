const API_URL = "http://YOUR_SERVER_IP:5000";

export async function sendImage(task, imageUri) {
  const formData = new FormData();

  formData.append("image", {
    uri: imageUri,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const response = await fetch(`${API_URL}/predict/${task}`, {
    method: "POST",
    body: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.json();
}
