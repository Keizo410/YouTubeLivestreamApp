import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  Button,
  ActivityIndicator,
} from "react-native";
import { Table, Row, Rows } from "react-native-table-component";
import { fetchChannels, fetchLivestreams, fetchYoutubers } from "@/utils/api";

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
          tableHead = ["ID", "Channel Name"];
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
    <>
      <View style={styles.buttonContainer}>
        <Button
          title="Youtubers"
          onPress={() => toggleButton("youtubers")}
          color="green"
        />
        <Button
          title="Channels"
          onPress={() => toggleButton("channels")}
          color="green"
        />
        <Button
          title="LiveStreams"
          onPress={() => toggleButton("livestreams")}
          color="green"
        />
      </View>
      <View style={styles.container}>
        <Text style={styles.text}>Ranking</Text>
        <Text style={styles.text}>{userView}</Text>;
      </View>
      <View style={styles.tableContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.text}>{error}</Text>
        ) : (
          <Table
            borderStyle={{ borderWidth: 4, borderColor: "teal" }}
            style={styles.table}
          >
            <Row
              data={data.tableHead}
              style={styles.head}
              textStyle={styles.text}
            />
            <Rows data={data.tableData} textStyle={styles.text} />
          </Table>
        )}
      </View>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#25292e",
    alignItems: "center",
    justifyContent: "center",
  },
  buttonContainer: {
    backgroundColor: "#25292e",
    flexDirection: "row",
    justifyContent: "space-around",
    padding: "1%",
  },
  tableContainer: {
    flex: 9,
    backgroundColor: "#25292e",
    paddingHorizontal: "30%",
  },
  head: {
    height: 40,
    backgroundColor: "darkblue",
  },
  table: {
    width: "100%",
  },
  text: {
    color: "#fff",
  },
  input: {
    height: 40,
    width: "30%",
    margin: 12,
    borderWidth: 1,
    padding: 10,
    color: "white",
    borderColor: "#fff",
  },
});
