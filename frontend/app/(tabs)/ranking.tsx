import React, { useState } from "react";
import { Text, View, StyleSheet, Button } from "react-native";
import { Table, Row, Rows } from "react-native-table-component";

const tableData = {
  tableHead: ["Crypto Name", "Value", "Mkt Cap"],
  tableData: [
    ["Bitcoin", "$44,331", "$839,702,328,904"],
    ["Ethereum", "$3000.9", "$359,080,563,225"],
    ["Tether", "$1", "$79,470,820,738"],
    ["BNB", "$413.44", "$69,446,144,361"],
    ["USD Coin", "$1", "$53,633,260,549"],
  ],
};

export default function ranking() {
  const [userView, setUserView] = useState("personal");
  const [data, setData] = useState(tableData);

  const toggle_button = (newView: React.SetStateAction<string>) => {
    setUserView(newView);
  };

  return (
    <>
      <View style={styles.buttonContainer}>
        <Button
          title="Your Tracking"
          onPress={() => toggle_button("personal")}
          color="green"
        />
        <Button
          title="World Ranking"
          onPress={() => toggle_button("global")}
          color="green"
        />
      </View>
      <View style={styles.container}>
        <Text style={styles.text}>Ranking</Text>
        {userView == "personal" ? (
          <Text style={styles.text}>personal</Text>
        ) : (
          <Text style={styles.text}>world</Text>
        )}
      </View>
      <View style={styles.tableContainer}>
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
    paddingTop: "5%",
  },
  tableContainer: {
    flex: 9,
    backgroundColor: "#25292e",
  },
  head: {
    height: 40,
    backgroundColor: "darkblue",
  },
  table: {
    width: "100%",
    // height: "100%",
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
