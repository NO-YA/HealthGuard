import { useEffect, useRef, useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { Camera } from "expo-camera";
import { sendImage } from "../services/api";

export default function CameraScreen() {
  const cameraRef = useRef(null);
  const [permission, requestPermission] = Camera.useCameraPermissions();
  const [result, setResult] = useState(null);

  useEffect(() => {
    requestPermission();
  }, []);

  if (!permission?.granted) {
    return <Text>Permission caméra requise</Text>;
  }

  const takePicture = async () => {
    const photo = await cameraRef.current.takePictureAsync();
    const response = await sendImage("diabetes", photo.uri);
    setResult(response);
  };

  return (
    <View style={styles.container}>
      <Camera style={styles.camera} ref={cameraRef} />
      <Button title="Analyser" onPress={takePicture} />
      {result && (
        <Text style={styles.result}>
          Diagnostic: {result.diagnosis} ({result.confidence}%)
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
  result: { padding: 16, fontSize: 18 },
});
