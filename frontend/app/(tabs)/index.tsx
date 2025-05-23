import {
  Text,
  View,
  StyleSheet,
  TextInput,
  Button,
  ActivityIndicator,
  Dimensions,
} from "react-native";
import { Link, router, useFocusEffect } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import { subscribeToYoutubers } from "@/app/api/api";
import React from "react";
import { LinearGradient } from "expo-linear-gradient";
import { useWindowDimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Index() {
  const [text, onChangeText] = useState("");
  const [loading, setLoading] = useState(false);
  // const { width } = useWindowDimensions();


  console.log(window.innerWidth);

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
    <SafeAreaView style={styles.container}>
    <LinearGradient
      colors={["#5fa8d3", "#a0d8ef", "#ffffff"]}
      style={styles.sectionContainer}
    >
      <Text style={{ ...styles.text, fontSize: Math.max(window.innerWidth * 0.016, 14) }}>
        Welcome to YouTube LiveStream Tracker
      </Text>
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <>
          <TextInput
            style={{ ...styles.input, fontSize: Math.max(window.innerWidth * 0.01, 14) }}
            onChangeText={onChangeText}
            value={text}
            placeholder="Paste your favorite YouTuber Handle (@...)"
          />
          <Button
            color="#5fa8d3"
            title="Request"
            onPress={() => handleSubscription(text)}
          />
        </>
      )}
    </LinearGradient>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
    container: {
    //entire page
    flex: 1,
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
    paddingBottom: 20,
  },
  sectionContainer: {
    //middle part
    flex: 2,
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
    display: "flex",
  },
  text: {
    color: "black",
    fontWeight: "bold",
  },
  button: {
    fontSize: 20,
    textDecorationLine: "underline",
    // color: "#fff",
  },
  input: {
    height: 40,
    width: "40%",
    margin: 12,
    borderWidth: 1,
    padding: 10,
    color: "black",
    fontWeight: "500",
  },
});
