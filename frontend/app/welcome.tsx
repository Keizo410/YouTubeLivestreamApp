import { Link, Stack } from "expo-router";
import React from "react";
import { View, StyleSheet, Text} from "react-native";

export default function Welcome() {
  return (
    <>
      <Stack.Screen options={{ title: "Welcome" }} />
      <View style={styles.container}>
        <Text style={{fontSize: 30, color: "black"}}>
            Welcome to the app.
        </Text>
        <Link href="/" style={styles.button}>
          Go to Home screen!
        </Link>
      </View>
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    fontSize: 20,
    textDecorationLine: "underline",
    color: "blue",
  },
});

