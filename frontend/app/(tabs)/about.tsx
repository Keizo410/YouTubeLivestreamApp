import { Text, View, StyleSheet, Dimensions, Image } from "react-native";
const { width } = Dimensions.get("window");
import { LinearGradient } from "expo-linear-gradient";

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      <LinearGradient
        colors={["#5fa8d3", "#a0d8ef", "#ffffff"]}
        style={styles.sectionContainer}
      >
          <View style={styles.sectionCardContainer}>
            <View style={styles.cardContainer}>
              <Text style={styles.cardText}>+5</Text>
            </View>
            <Text
              numberOfLines={1}
              adjustsFontSizeToFit
              style={styles.descriptionText}
            >
              Registered Channels
            </Text>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Keep track of your favorite YouTube channels and their
              livestreams.
            </Text>
          </View>
          <View style={styles.sectionCardContainer}>
            <Image
              source={require("../../assets/images/data-analytics.png")}
              style={{ ...styles.cardContainer }}
              resizeMode="contain"
            ></Image>
            <Text
              numberOfLines={1}
              adjustsFontSizeToFit
              style={styles.descriptionText}
            >
              Live Chat Analysis
            </Text>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Analyze live chat messages and identify trending topics.{" "}
            </Text>
          </View>
          <View style={styles.sectionCardContainer}>
            <Image
              source={require("../../assets/images/money-transfer.png")}
              style={{ ...styles.cardContainer }}
              resizeMode="contain"
            ></Image>
            <Text
              numberOfLines={1}
              adjustsFontSizeToFit
              style={styles.descriptionText}
            >
              Super Chat Donations
            </Text>
            <Text
              numberOfLines={3}
              adjustsFontSizeToFit
              style={styles.semiDescriptionText}
            >
              Monitor donations and engagement from viewers.
            </Text>
          </View>
      </LinearGradient>
    </View>
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
    justifyContent: "space-around",
    display: "flex",
    flexDirection: "row",
    paddingHorizontal: 90,
  },
  sectionCardContainer: {
    //each card sections
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: 150,
  },
  cardContainer: {
    //individual image&number card section
    width: width * 0.2,
    height: width * 0.15,
    flex: 1,
    alignSelf: "center",
    justifyContent: "center",
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
  semiDescriptionText: {
    color: "black",
    fontSize: width * 0.009,
    fontWeight: "500",
    flex: 1,
    textAlign: "left",
    width: width * 0.2,
  },
  cardText: {
    //channel number
    fontSize: width * 0.05,
    fontWeight: "bold",
    textAlign: "center",
  },
});
