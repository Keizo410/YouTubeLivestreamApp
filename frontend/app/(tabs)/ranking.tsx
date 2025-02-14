import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  Button,
  ActivityIndicator,
  Dimensions,
  TouchableOpacity
} from "react-native";
import { Table, Row, Rows } from "react-native-table-component";
import { fetchChannels, fetchLivestreams, fetchYoutubers } from "@/utils/api";
import { LinearGradient } from "expo-linear-gradient";
const { width, height } = Dimensions.get("window");

export default function Ranking() {
  const [userView, setUserView] = useState("youtubers");
  const [data, setData] = useState({
    tableHead: [],
    tableData: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true);
    setError(null);

    const fetchData = async () => {
      try {
        let tableData;
        let tableHead;

        if (userView === "youtubers") {
          tableData = await fetchYoutubers();
          tableHead = ["ID", "Name"];
        } else if (userView === "channels") {
          tableData = await fetchChannels();
          tableHead = ["ID", "Channel Name", "Youtuber"];
        } else if (userView === "livestreams") {
          tableData = await fetchLivestreams();
          tableHead = [
            "ID",
            "Time",
            "Date",
            "Channel ID",
            "Listener ID",
            "Donation",
            "Comment",
          ];
        }

        setData({ tableHead, tableData });
      } catch (err) {
        setError(err?.message ?? "error occured");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userView]);

  const toggleButton = (newView: React.SetStateAction<string>) => {
    setUserView(newView);
  };

  return (
    <View style={styles.container}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={userView==="youtubers" ? styles.selectedButton : styles.button} onPress={()=>toggleButton("youtubers")}>
          <Text style={styles.buttonText}>YouTubers</Text>
        </TouchableOpacity>
        <TouchableOpacity style={userView==="channels" ? styles.selectedButton : styles.button} onPress={()=>toggleButton("channels")}>
          <Text style={styles.buttonText}>Channels</Text>
        </TouchableOpacity>
        <TouchableOpacity style={userView==="livestreams" ? styles.selectedButton : styles.button} onPress={()=>toggleButton("livestreams")}>
          <Text style={styles.buttonText}>LiveStreams</Text>
        </TouchableOpacity>
      </View>
      {/* <View style={styles.container}>
        <Text style={styles.text}>Ranking</Text>
        <Text style={styles.text}>{userView}</Text>
      </View> */}
      <View style={styles.tableContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.headText}>{error}</Text>
        ) : (
          <Table borderStyle={styles.tableStyle} style={styles.table}>
            <Row
              data={data.tableHead}
              style={styles.head}
              textStyle={styles.headText}
            />
            <Rows data={data.tableData} textStyle={styles.dataText} />
          </Table>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    display: "flex",
    width: "100%",
    height: "100%",
    backgroundColor: "white"
  },
  buttonContainer: {
    flex: 1,
    width: "100%",
    flexDirection: "row",
    justifyContent: "space-around",
    padding: "1%",
  },
  tableContainer: {
    flex: 9,
    width: "70%",
  },
  tableStyle: {
    borderWidth: 3,
    borderColor: "#5fa8d3",
  },
  head: {
    height: 40,
  },
  table: {
  },
  headText: {
    color: "black",
    fontSize: width * 0.012,
    fontWeight: "bold",
    textAlign:"center"
  },
  dataText:{
    color: "black",
    fontSize: width * 0.01,
    fontWeight: "bold",
    textAlign:"center"
  },
  button:{
    backgroundColor: "#5fa8d3",
    width: width*0.07,
    height: height * 0.05,
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },
  buttonText: {
    color: "white",
    fontSize: width * 0.01,
    fontWeight: "bold",
  },
  selectedButton: {
    backgroundColor: "#3b82a0",
    width: width*0.07,
    height: height * 0.05,
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  }
});
