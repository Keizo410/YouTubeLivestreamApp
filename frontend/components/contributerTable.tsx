import React from "react";
import { SafeAreaView, View, Text, useWindowDimensions } from "react-native";
import { Rows } from "react-native-table-component";
import { StyleSheet } from "react-native";

interface tableTypeProps {
  data: any;
}

export default function ContributerTableComponent({ data }: tableTypeProps) {
  const { width, height } = useWindowDimensions();
  const styles = StyleSheet.create({
    tableColumns: {
      display: "flex",
      flexDirection: "row",
      justifyContent: "space-around",
      height: height,
      paddingTop: 30,
    },
    onlineStatusColumn: {
      display: "flex",
      width: width * 0.1,
      alignItems: "center",
    },
    nameColumn: {
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
      <View style={styles.nameColumn}>
        <Text style={styles.headText}>Names</Text>
        <Rows data={data.tableData} textStyle={styles.dataText} />
      </View>
    </SafeAreaView>
  );
}
