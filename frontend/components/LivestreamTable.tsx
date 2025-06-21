import React from "react";
import { SafeAreaView, View, Text, useWindowDimensions } from "react-native";
import { Rows } from "react-native-table-component";
import { StyleSheet } from "react-native";

interface tableTypeProps {
  data: any;
}

export default function LivestreamTableComponent({ data }: tableTypeProps) {
  const { width, height } = useWindowDimensions();
  const styles = StyleSheet.create({
    tableColumns: {
      display: "flex",
      flexDirection: "row",
      justifyContent: "space-around",
      height: height,
      paddingTop: 30,
    },
    column: {
      display: "flex",
      width: width * 0.1,
      alignItems: "center",
    },
    headText: {
      color: "black",
      fontSize: width * 0.012,
      fontWeight: "bold",
      borderBottomWidth: 1,
      // backgroundColor: "red",
      width: width * 0.1,
      textAlign: "center",
    },
    dataText: {
      color: "black",
      fontSize: width * 0.012,
      fontWeight: "bold",
    },
  });

  return (
    <SafeAreaView style={styles.tableColumns}>
      <View style={styles.column}>
        <Text style={styles.headText}>Time</Text>
        <Rows
          data={data.tableData.map((row: any[]) => [row[0]])}
          textStyle={styles.dataText}
        />
      </View>

      <View style={styles.column}>
        <Text style={styles.headText}>Date</Text>
        <Rows
          data={data.tableData.map((row: any[]) => [row[1]])}
          textStyle={styles.dataText}
        />
      </View>
      <View style={styles.column}>
        <Text style={styles.headText}>Donation</Text>
        <Rows
          data={data.tableData.map((row: any[]) => [row[2]])}
          textStyle={styles.dataText}
        />
      </View>
      <View style={styles.column}>
        <Text style={styles.headText}>Comments</Text>
        <Rows
          data={data.tableData.map((row: any[]) => [row[3]])}
          textStyle={styles.dataText}
        />
      </View>
    </SafeAreaView>
  );
}
