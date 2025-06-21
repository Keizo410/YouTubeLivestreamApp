import React, { useEffect, useState } from "react";
import {
  View,
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import ChannelView from "../dashboardViews/ChannelView";
import LivestreamView from "../dashboardViews/LiveStreamView";
import { useWindowDimensions } from "react-native";
import {
  fetchChannels,
  fetchListeners,
  fetchLivestreams,
  fetchLivestreamsBarSummary,
  fetchLivestreamsChartSummary,
  fetchYoutubers,
} from "../api/api";
import ContributerView from "../dashboardViews/ContributerView";

export default function Ranking() {
  const [userView, setUserView] = useState("Contributers");
  const { width, height } = useWindowDimensions();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [totalSalesBarData, setTotalSalesBarData] = useState([]);
  const [data, setData] = useState({
    tableHead: [],
    tableData: [],
  });
  const [channelArray, setChannelArray] = useState<string[]>([]);
  const [livestreamScreen, setLivestreamScreen] = useState("livestream");

  const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: "white" },
    buttonContainer: {
      flexDirection: "row",
      justifyContent: "space-around",
      // padding: "1%",
      // backgroundColor: "red",
      height: height * 0.05,
      borderBottomWidth: 1,
      borderBottomColor: "black",
    },
    dataContainer: {
      height: height,
      paddingTop: 30,
    },
    button: {
      // backgroundColor: "#5fa8d3",
      opacity: 0.3,
      width: width * 0.25,
      alignItems: "center",
      justifyContent: "center",
    },
    selectedButton: {
      // backgroundColor: "#5fa8d3",
      width: width * 0.25,
      alignItems: "center",
      justifyContent: "center",
    },
    buttonText: {
      color: "black",
      fontSize: width * 0.01,
      fontWeight: "bold",
    },
    errorText: {
      color: "black",
      fontSize: width * 0.03,
      fontWeight: "bold",
    },
  });

  const renderCurrentView = () => {
    switch (userView) {
      case "Contributers":
        return <ContributerView data={data} />;
      case "Channels":
        return <ChannelView data={data} />;
      case "Livestreams":
        return <LivestreamView data={data} />;
      default:
        return null;
    }
  };
  useEffect(() => {
    setLoading(true);
    setError(null);

    const fetchTableData = async () => {
      try {
        let tableData;
        let tableHead;

        if (userView === "Contributers") {
          tableData = await fetchListeners();
          tableHead = ["Name", "Donation"];
        } else if (userView === "Channels") {
          tableData = await fetchChannels();
          tableHead = ["ID", "Channel Name", "Youtuber", "Status"];
        } else if (userView === "Livestreams") {
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
    <SafeAreaView style={styles.container}>
      <View style={styles.buttonContainer}>
        {["Contributers", "Channels", "Livestreams"].map((view) => (
          <TouchableOpacity
            key={view}
            style={userView === view ? styles.selectedButton : styles.button}
            onPress={() => setUserView(view)}
          >
            <Text style={styles.buttonText}>{view}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <View style={styles.dataContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.errorText}>{error}</Text>
        ) : (
          renderCurrentView()
        )}
      </View>
    </SafeAreaView>
  );
}
