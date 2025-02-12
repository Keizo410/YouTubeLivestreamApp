import {
  Text,
  View,
  StyleSheet,
  TextInput,
  Button,
  ActivityIndicator,
} from "react-native";
import { Link, router } from "expo-router";
import { useEffect, useState } from "react";
import { subscribeToYoutubers } from "@/utils/api";
import React from "react";

export default function Index() {
  const [text, onChangeText] = useState(
    "Paste your favorite YouTuber Handle (@...)"
  );
  const [loading, setLoading] = useState(false);

  const handleSubscription = async (youtuber: string) => {
    setLoading(true);

    try {
      const [response, data] = await subscribeToYoutubers(youtuber);
      if (response.status === 201) {
        router.push({
          pathname: "/success",
          params: { id: data.message },
        });
      } else {
        router.push("/failedSubscription");
      }
    } catch (error) {
      console.log("Error:", error);
      router.push("/failedSubscription");
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Welcome to YouTube LiveStream Tracker</Text>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <>
          <TextInput
            style={styles.input}
            onChangeText={onChangeText}
            value={text}
            placeholder="Enter YouTuber name"
          />
          <Button title="Request" onPress={() => handleSubscription(text)} />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#25292e",
    alignItems: "center",
    justifyContent: "center",
  },
  text: {
    color: "#fff",
  },
  button: {
    fontSize: 20,
    textDecorationLine: "underline",
    color: "#fff",
  },
  input: {
    height: 40,
    width: "40%",
    margin: 12,
    borderWidth: 1,
    padding: 10,
    color: "white",
    borderColor: "#fff",
  },
});
