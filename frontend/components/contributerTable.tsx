import React, { useState } from "react";
import {
  SafeAreaView,
  View,
  Text,
  useWindowDimensions,
  TextInput,
} from "react-native";
import { Rows } from "react-native-table-component";
import { StyleSheet } from "react-native";
import { SearchBar } from "react-native-screens";

interface tableTypeProps {
  data: any;
}

export default function ContributerTableComponent({ data }: tableTypeProps) {
  const [text, contributerhName] = useState("");

  const { width, height } = useWindowDimensions();
  const styles = StyleSheet.create({
    tableContainer: {
      display: "flex",
      flexDirection: "column",
      height: height,
    },
    tableColumns: {
      display: "flex",
      flexDirection: "row",
      justifyContent: "space-around",
      height: height,
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
      paddingTop: 30,
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
    input: {
      borderColor: "black",
      borderWidth: 1,
      height: "100%",
      fontSize: width * 0.015,
      textAlign: "center",
      opacity: 0.5,
    },
    searchBar: {
      height: height * 0.05,
      width: width * 0.3,
      alignSelf: "center",
    },
  });

  return (
    <SafeAreaView style={styles.tableContainer}>
      <View style={styles.searchBar}>
        <TextInput
          style={[styles.input, text !== "" && { color: "black", opacity: 1 }]}
          onChangeText={contributerhName}
          value={text}
          placeholder="Search Contributer Name"
        />
      </View>
      <View style={styles.tableColumns}>
        <View style={styles.nameColumn}>
          <Text style={styles.headText}>Names</Text>
          <Rows
            data={data.tableData.map((row: any[]) => [row[0]])}
            textStyle={styles.dataText}
          />
        </View>
        <View style={styles.nameColumn}>
          <Text style={styles.headText}>Total Donation</Text>
          <Rows
            data={data.tableData.map((row: any[]) => [row[1]])}
            textStyle={styles.dataText}
          />
        </View>
      </View>
    </SafeAreaView>
  );
}
