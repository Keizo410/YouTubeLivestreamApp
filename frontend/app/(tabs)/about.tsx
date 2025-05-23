import {
  Text,
  View,
  StyleSheet,
  Dimensions,
  Image,
  SafeAreaView,
  useWindowDimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { useEffect, useState } from "react";
import { fetchChannelNum } from "@/app/api/api";

export default function AboutScreen() {
  const [channelNum, setChannelNum] = useState("+5");
  const { width } = useWindowDimensions();

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
    justifyContent: "space-around",
    display: "flex",
    flexDirection: "row",
  },
  sectionCardContainer: {
    //each card sections
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: 150,
  },
  descriptionText: {
    color: "black",
    fontSize: width * 0.016,
    fontWeight: "bold",
    flex: 1,
    alignContent: "center",
    textAlign: "center",
    width: width * 0.2,
  },
  semiDescriptionContainer: {
    flex: 1,
  },
  semiDescriptionText: {
    color: "black",
    fontSize: width * 0.009,
    fontWeight: "500",
    textAlign: "center",
    width: width * 0.2,
  },
  imageAndSubContainer: {
    //channel number
    fontSize: width * 0.05,
    height: width*0.15,
    width: "100%",
    fontWeight: "bold",
    textAlign: "center",
    alignContent: "center"
  },
});

  useEffect(() => {
    const fetchData = async () => {
      try {
        let data = await fetchChannelNum();
        setChannelNum(data);
      } catch (err) {
        console.log(err);
      }
    };
    fetchData();
  }, [channelNum]);

  return (
    <SafeAreaView style={styles.container}>
      <LinearGradient
        colors={["#5fa8d3", "#a0d8ef", "#ffffff"]}
        style={styles.sectionContainer}
      >
        <View style={styles.sectionCardContainer}>
            <Text style={styles.imageAndSubContainer}>+{channelNum}</Text>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.descriptionText}
          >
            Registered Channels
          </Text>
          <View style={styles.semiDescriptionContainer}>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Keep track of your favorite YouTube channels and their
              livestreams.
            </Text>
          </View>
        </View>
        <View style={styles.sectionCardContainer}>
          <Image
            source={require("../../assets/images/data-analytics.png")}
            style={{ ...styles.imageAndSubContainer }}
            resizeMode="contain"
          ></Image>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.descriptionText}
          >
            Live Chat Analysis
          </Text>
          <View style={styles.semiDescriptionContainer}>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Analyze live chat messages and identify trending topics.{" "}
            </Text>
          </View>
        </View>
        <View style={styles.sectionCardContainer}>
          <Image
            source={require("../../assets/images/money-transfer.png")}
            style={{ ...styles.imageAndSubContainer }}
            resizeMode="contain"
          ></Image>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.descriptionText}
          >
            Super Chat Donations
          </Text>
          <View style={styles.semiDescriptionContainer}>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Monitor donations and engagement from viewers.
            </Text>
          </View>
        </View>
      </LinearGradient>
    </SafeAreaView>
  );
}


