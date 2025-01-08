import React, { useEffect, useState } from "react";
import { Text, View, StyleSheet, Button, ActivityIndicator } from "react-native";
import { Table, Row, Rows } from "react-native-table-component";


export default function Ranking() {
  const [userView, setUserView] = useState("personal");
  const [data, setData] = useState({
    tableHead: ["ID", "NAME"],
    tableData: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch YouTubers data from API
    fetch("http://localhost:8000/api/subscriptions/youtubers") // Replace with your API endpoint
      .then((response) => response.json())
      .then((responseData) => {
        // Assuming responseData is an array of YouTubers with only name and id
        const tableData = responseData.map((youtuber: { id: any; name: any; }) => [
          youtuber.id, // Assuming 'id' is the unique identifier
          youtuber.name, // Assuming 'name' is the YouTuber's name
        ]);
        setData({tableHead: ["ID", "Name"], tableData });
        setLoading(false);
      })
      .catch((error) => {
        setError("error");
        setLoading(false);
      });
  }, []);

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
      {/* <View style={styles.tableContainer}>
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
      </View> */}
      <View style={styles.tableContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.text}>{error}</Text>
        ) : (
          <Table borderStyle={{ borderWidth: 4, borderColor: "teal" }} style={styles.table}>
            <Row data={data.tableHead} style={styles.head} textStyle={styles.text} />
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
// import React, { useState, useEffect } from "react";
// import { Text, View, StyleSheet, Button, ActivityIndicator } from "react-native";
// import { Table, Row, Rows } from "react-native-table-component";

// export default function Ranking() {
//   const [userView, setUserView] = useState("personal");
//   const [data, setData] = useState({ tableHead: ["ID", "Name"], tableData: [] });
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   const toggle_button = (newView) => {
//     setUserView(newView);
//   };

//   useEffect(() => {
//     // Fetch YouTubers data from API
//     fetch("http://localhost:8000/api/subscriptions/youtubers") // Replace with your API endpoint
//       .then((response) => response.json())
//       .then((responseData) => {
//         // Assuming responseData is an array of YouTubers with only name and id
//         const tableData = responseData.map((youtuber: { id: any; name: any; }) => [
//           youtuber.id, // Assuming 'id' is the unique identifier
//           youtuber.name, // Assuming 'name' is the YouTuber's name
//         ]);
//         setData({ tableHead: ["ID", "Name"], tableData });
//         setLoading(false);
//       })
//       .catch((error) => {
//         setError("Failed to fetch data");
//         setLoading(false);
//       });
//   }, []);

//   return (
//     <>
//       <View style={styles.buttonContainer}>
//         <Button
//           title="Your Tracking"
//           onPress={() => toggle_button("personal")}
//           color="green"
//         />
//         <Button
//           title="World Ranking"
//           onPress={() => toggle_button("global")}
//           color="green"
//         />
//       </View>

//       <View style={styles.container}>
//         <Text style={styles.text}>Ranking</Text>
//         {userView === "personal" ? (
//           <Text style={styles.text}>Personal View</Text>
//         ) : (
//           <Text style={styles.text}>World View</Text>
//         )}
//       </View>

//       <View style={styles.tableContainer}>
//         {loading ? (
//           <ActivityIndicator size="large" color="#0000ff" />
//         ) : error ? (
//           <Text style={styles.text}>{error}</Text>
//         ) : (
//           <Table borderStyle={{ borderWidth: 4, borderColor: "teal" }} style={styles.table}>
//             <Row data={data.tableHead} style={styles.head} textStyle={styles.text} />
//             <Rows data={data.tableData} textStyle={styles.text} />
//           </Table>
//         )}
//       </View>
//     </>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: "#25292e",
//     alignItems: "center",
//     justifyContent: "center",
//   },
//   buttonContainer: {
//     backgroundColor: "#25292e",
//     flexDirection: "row",
//     justifyContent: "space-around",
//     paddingTop: "5%",
//   },
//   tableContainer: {
//     flex: 9,
//     backgroundColor: "#25292e",
//   },
//   head: {
//     height: 40,
//     backgroundColor: "darkblue",
//   },
//   table: {
//     width: "100%",
//   },
//   text: {
//     color: "#fff",
//   },
//   input: {
//     height: 40,
//     width: "30%",
//     margin: 12,
//     borderWidth: 1,
//     padding: 10,
//     color: "white",
//     borderColor: "#fff",
//   },
// });
