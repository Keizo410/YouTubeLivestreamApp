import React from "react";
import { Dimensions } from "react-native";
import { Table, Row, Rows } from "react-native-table-component";
import { StyleSheet } from "react-native";

const { width, height } = Dimensions.get("window");

interface tableTypeProps {
  data: any;
}

export default function TableComponent({ data }: tableTypeProps) {
  return (
    <Table borderStyle={styles.tableStyle}>
      <Row
        data={data.tableHead}
        style={styles.head}
        textStyle={styles.headText}
      />
      <Rows data={data.tableData} textStyle={styles.dataText} />
    </Table>
  );
}

const styles = StyleSheet.create({
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
  headText: {
    color: "black",
    fontSize: width * 0.012,
    fontWeight: "bold",
    textAlign: "center",
  },
  dataText: {
    color: "black",
    fontSize: width * 0.01,
    fontWeight: "bold",
    textAlign: "center",
  },
});
