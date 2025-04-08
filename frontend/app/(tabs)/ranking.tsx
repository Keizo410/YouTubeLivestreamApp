import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  ActivityIndicator,
  Dimensions,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import {
  fetchChannels,
  fetchLivestreams,
  fetchLivestreamsBarSummary,
  fetchLivestreamsChartSummary,
  fetchYoutubers,
} from "@/utils/api";
import TableComponent from "@/components/table";
import ChartComponent from "../../components/chart";
import BarComponent from "@/components/bar";
import { SafeAreaView } from "react-native-safe-area-context";

const { width, height } = Dimensions.get("window");

export default function Ranking() {
  const [userView, setUserView] = useState("youtubers");
  const [chartData, setChartData] = useState([]);
  const [totalSalesBarData, setTotalSalesBarData] = useState([]);
  const [data, setData] = useState({
    tableHead: [],
    tableData: [],
  });
  const [channelArray, setChannelArray] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [livestreamScreen, setLivestreamScreen] = useState("livestream");
  const toggleButton = (newView: React.SetStateAction<string>) => {
    setUserView(newView);
  };
  const toggleChartViewButton = (newView: React.SetStateAction<string>) => {
    setLivestreamScreen(newView);
  };

  useEffect(() => {
    setLoading(true);
    setError(null);

    const fetchTableData = async () => {
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

    fetchTableData();
  }, [userView]);

  useEffect(() => {
    const registerChannelNames = () => {
      const channelNames = new Set<string>();
      for (let item of chartData) {
        if (item) {
          for (let key of Object.keys(item)) {
            if (key !== "date") {
              channelNames.add(key);
            }
          }
        }
      }
      setChannelArray([...channelNames]);
    };

    if (chartData && chartData.length > 0) {
      registerChannelNames();
    }
  }, [chartData]);

  useEffect(() => {
    const fetchBarData = async () => {
      try {
        let rawData;

        rawData = await fetchLivestreamsBarSummary();

        setTotalSalesBarData(rawData);
      } catch (err) {
        setError(err?.message ?? "Error at fetchChartData");
      } finally {
        setLoading(false);
      }
    };

    fetchBarData();
  }, [livestreamScreen === "bar"]);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        let rawData;

        if (userView === "livestreams") {
          rawData = await fetchLivestreamsChartSummary();
        }

        setChartData(rawData);
      } catch (err) {
        setError(err?.message ?? "Error at fetchChartData");
      } finally {
        setLoading(false);
      }
    };

    fetchChartData();
  }, [livestreamScreen === "chart"]);

  return (
    <View style={styles.container}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={
            userView === "youtubers" ? styles.selectedButton : styles.button
          }
          onPress={() => toggleButton("youtubers")}
        >
          <Text style={styles.buttonText}>YouTubers</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={
            userView === "channels" ? styles.selectedButton : styles.button
          }
          onPress={() => toggleButton("channels")}
        >
          <Text style={styles.buttonText}>Channels</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={
            userView === "livestreams" ? styles.selectedButton : styles.button
          }
          onPress={() => toggleButton("livestreams")}
        >
          <Text style={styles.buttonText}>LiveStreams</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.tableContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.headText}>{error}</Text>
        ) : userView != "livestreams" ? (
          <TableComponent data={data} />
        ) : (
          <View style={styles.chartBarContainer}>
            <SafeAreaView style={styles.chartBarChildContainer}>
              <ScrollView horizontal={true}>
                {livestreamScreen === "chart" ? (
                  <ChartComponent
                    chartData={chartData}
                    channelArray={channelArray}
                  />
                ) : (
                  <BarComponent data={totalSalesBarData} />
                )}
              </ScrollView>
            </SafeAreaView>
            <View style={styles.chartBarButtonContainer}>
              <TouchableOpacity
                style={
                  livestreamScreen === "chart"
                    ? styles.selectedButton
                    : styles.button
                }
                onPress={() => toggleChartViewButton("chart")}
              >
                <Text style={styles.buttonText}>Chart</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={
                  livestreamScreen === "livestream"
                    ? styles.selectedButton
                    : styles.button
                }
                onPress={() => toggleChartViewButton("livestream")}
              >
                <Text style={styles.buttonText}>Bar</Text>
              </TouchableOpacity>
            </View>
          </View>
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
    backgroundColor: "white",
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
    width: "80%",
    display: "flex",
  },
  head: {
    height: 40,
  },
  headText: {
    color: "black",
    fontSize: width * 0.012,
    fontWeight: "bold",
    textAlign: "center",
  },
  button: {
    backgroundColor: "#5fa8d3",
    width: width * 0.07,
    height: height * 0.05,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    color: "white",
    fontSize: width * 0.01,
    fontWeight: "bold",
  },
  selectedButton: {
    backgroundColor: "#3b82a0",
    width: width * 0.07,
    height: height * 0.05,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  chartBarContainer: {
    flex: 1,
    flexDirection: "row",
    display: "flex",
    width: "100%",
  },
  chartBarChildContainer: {
    flex: 9,
  },
  chartBarButtonContainer: {
    flex: 1,
    alignItems: "center",
  },
});
