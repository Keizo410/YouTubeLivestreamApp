import { Link, Stack } from "expo-router";
import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function failedSubscription() {
  return (
    <>
      <Stack.Screen options={{ title: "FAILURE" }} />
      <View style={styles.container}>
        <Text style={styles.text}>Subscription Failure:/</Text>
        <Link href="/" style={styles.button}>
          Go back to Home screen!
        </Link>
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#25292e',
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: "#fff",
    fontSize: 20,
  },
  button: {
    fontSize: 20,
    textDecorationLine: "underline",
    color: "#fff",
  },
});
