import {
  Text,
  View,
  StyleSheet,
  Dimensions,
  Image
} from "react-native";
const { width } = Dimensions.get("window");
import { LinearGradient } from "expo-linear-gradient";

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.headerContainer}>
        <Text numberOfLines={1} adjustsFontSizeToFit style={styles.headerText}>
          Gain Insights from YouTube Live Chats & Super Chats
        </Text>
      </View>
      <LinearGradient
        colors={["#5fa8d3", "#a0d8ef", "#ffffff"]}
        style={styles.semiHeaderContainer}
      >
        <View style={styles.semiHeaderCardContainer}>
          <View style={styles.cardContainer}>
            <Text style={styles.cardText}>+5</Text>
          </View>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.semiHeaderText}
          >
            Registered Channels
          </Text>
          <Text
            numberOfLines={3}
            adjustsFontSizeToFit
            style={styles.semiHeaderDescText}
          >
            Keep track of your favorite YouTube channels and their livestreams.
          </Text>
        </View>
        <View style={styles.semiHeaderCardContainer}>
          <Image
            source={require("../../assets/images/analysis.png")}
            style={{...styles.cardContainer,   }}
            resizeMode="contain" 
          ></Image>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.semiHeaderText}
          >
            Live Chat Analysis
          </Text>
          <Text
            numberOfLines={3}
            adjustsFontSizeToFit
            style={styles.semiHeaderDescText}
          >
            Analyze live chat messages and identify trending topics.{" "}
          </Text>
        </View>
        <View style={styles.semiHeaderCardContainer}>
          <Image source={require("../../assets/images/donation.png")}
            style={{...styles.cardContainer,   }}
            resizeMode="contain" 
            >

          </Image>
          <Text
            numberOfLines={1}
            adjustsFontSizeToFit
            style={styles.semiHeaderText}
          >
            Super Chat Donations
          </Text>
          <Text
            numberOfLines={3}
            adjustsFontSizeToFit
            style={styles.semiHeaderDescText}
          >
            Monitor donations and engagement from viewers.
          </Text>
        </View>
      </LinearGradient>

      <View style={styles.contentContainer}>
        <Text
          numberOfLines={3}
          adjustsFontSizeToFit
          style={styles.contentHeaderText}
        >
          Track, analyze, and gain insights from YouTube livestreams in
          real-time. This app lets you monitor Super Chats, analyze live chat
          interactions, and visualize data trends effortlessly.
        </Text>
        <Text style={styles.featureHeaderText}>Key Features:</Text>
        <View style={styles.featureList}>
          <Text style={styles.featureItem}>
            🔴 Automatic Livestream Tracking
          </Text>
          <Text style={styles.featureItem}>💬 Live Chat Analysis</Text>
          <Text style={styles.featureItem}>💰 Super Chat Monitoring</Text>
          <Text style={styles.featureItem}>📊 Data Visualization</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {//entire page
    flex: 1,
    backgroundColor: "white",
    justifyContent: "center",
    alignItems: "center",
    paddingBottom: 20,
  },
  headerContainer: {//Header 
    flex: 1,
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#5fa8d3",
  },
  semiHeaderContainer: {//middle part
    flex: 2,
    width: "100%",
    justifyContent: "space-around",
    display: "flex",
    flexDirection: "row",
    paddingHorizontal: 90,
  },
  contentContainer: {//bottom part(from white)
    flex: 3,
    width: "80%",
  },
  semiHeaderCardContainer: {//each card sections
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    borderRadius: 30,
  },
  cardContainer: {//individual image&number card section
    width: width * 0.15,
    height: width * 0.15,
    flex: 2,
    borderRadius: 30,
    alignSelf: "center",
    justifyContent: "center",
  },
  headerText: {
    color: "black",
    fontSize: width * 0.03,
    fontWeight: "bold",
  },
  semiHeaderText: {
    color: "black",
    fontSize: width * 0.016,
    fontWeight: "bold",
    flex: 1,
    alignContent: "center",
    textAlign: "center",
    width: width * 0.2,
  },
  semiHeaderDescText: {
    color: "black",
    fontSize: width * 0.009,
    fontWeight: "500",
    flex: 1,
    textAlign: "left",
    width: width * 0.13,
  },
  cardText: {//channel number
    fontSize: width * 0.05,
    fontWeight: "bold",
    textAlign: "center",
  },
  contentHeaderText: {
    color: "black",
    fontSize: width * 0.016,
    fontWeight: "bold",
    paddingHorizontal: 50,
    paddingTop: 30,
  },
  featureList: {
    width: "80%",
    marginTop: 20,
  },
  featureItem: {
    color: "black",
    fontSize: width * 0.012,
    fontWeight: "bold",
    paddingHorizontal: 50,
    paddingTop: 10,
  },
  featureHeaderText: {
    color: "black",
    fontSize: width * 0.013,
    fontWeight: "bold",
    paddingHorizontal: 50,
    paddingTop: 30,
  },
});
