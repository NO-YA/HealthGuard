import { useRef, useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { Camera, CameraType, useCameraPermissions } from "expo-camera";

const API_URL = "http://TON_IP:5000";

export default function CameraScreen() {
  const cameraRef = useRef<Camera | null>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [result, setResult] = useState<any>(null);

  if (!permission) {
    return <Text>Chargement permissions...</Text>;
  }

  if (!permission.granted) {
    return (
      <View style={styles.permissionContainer}>
        <Text style={styles.text}>
          Nous avons besoin de la caméra pour analyser l’image
        </Text>
        <Button title="Autoriser la caméra" onPress={requestPermission} />
      </View>
    );
  }

  const takePicture = async () => {
    const photo = await cameraRef.current?.takePictureAsync();
    if (!photo) return;

    const formData = new FormData();
    formData.append("image", {
      uri: photo.uri,
      name: "image.jpg",
      type: "image/jpeg",
    } as any);

    const res = await fetch(`${API_URL}/predict/diabetes`, {
      method: "POST",
      body: formData,
      headers: { "Content-Type": "multipart/form-data" },
    });

    const json = await res.json();
    setResult(json);
  };

  return (
    <View style={styles.container}>
      <Camera ref={cameraRef} style={styles.camera} type={CameraType.back} />
      <Button title="Analyser" onPress={takePicture} />
      {result && (
        <Text style={styles.result}>
          Diagnostic : {result.diagnosis} ({result.confidence}%)
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  result: { padding: 16, fontSize: 18 },
  permissionContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  text: {
    textAlign: "center",
    marginBottom: 10,
    fontSize: 16,
  },
});
