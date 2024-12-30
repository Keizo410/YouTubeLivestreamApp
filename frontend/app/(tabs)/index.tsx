import { Text, View, StyleSheet, TextInput, Button } from "react-native";
import { Link, router } from "expo-router";
import { useEffect, useState } from "react";

export default function Index() {
  const [text, onChangeText] = useState("Paste your favorite YouTuber Handle (@...)");
  
  const subscribeToYoutuber = async (youtuber: string) => {
    try{
      const response = await fetch(`http://localhost:8000/api/subscriptions`
        ,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({youtuber:youtuber})
      })
      const data = await response.json();
      if(response.status==201){
        router.push({
          pathname: "/success",
          params: {id: data.message}
        });
      }else{
        router.push("/failedSubscription")
      }
    }catch (error){
      console.log("Error:", error);
      router.push("/failedSubscription")
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Welcome to YouTube LiveStream Tracker</Text>
      <TextInput
        style={styles.input}
        onChangeText={onChangeText}
        value={text}
      />
      <Button title="Request" onPress={() => subscribeToYoutuber(text)}/>
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
