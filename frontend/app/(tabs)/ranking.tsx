import React, { useEffect, useState } from "react";
import {
  Text,
  View,
  StyleSheet,
  Button,
  ActivityIndicator,
} from "react-native";
import { Table, Row, Rows } from "react-native-table-component";

export default function Ranking() {
  const [userView, setUserView] = useState("youtuber");
  const [data, setYoutuberData] = useState({
    tableHead: ["ID", "NAME"],
    tableData: [],
  });
  
  const [livestreamdata, setLivestreamData] = useState({
    tableHead: ["ID", "Time", "Date", "channelID", "ListenerID", "Donation", "Comment"],
    tableData: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if(userView==="youtubers") get_youtubers();
    if(userView==="channels") get_channels();
    if(userView==="livestreams") get_livestreams();
  }, [userView]);


  const get_channels = () => {
    // Fetch YouTubers data from API
    fetch("http://localhost:8000/api/subscriptions/channels") // Replace with your API endpoint
      .then((response) => response.json())
      .then((responseData) => {
        // Assuming responseData is an array of YouTubers with only name and id
        const tableData = responseData.map(
          (channel: { id: any; name: any; }) => [
            channel.id, // Assuming 'id' is the unique identifier
            channel.name, // Assuming 'name' is the YouTuber's name
          ]
        );
        setYoutuberData({ tableHead: ["ID", "Name"], tableData });
        setLoading(false);
      })
      .catch((error) => {
        setError("error");
        setLoading(false);
      });
  }

  //not working
  const get_livestreams = () => {
    fetch("http://localhost:8000/api/livestreams") // Replace with your API endpoint
    .then((response) => response.json())
    .then((responseData) => {
      // Assuming responseData is an array of YouTubers with only name and id
      const tableData = responseData.map(
        (livestreams: { id: any; currentTime: any; date: any; channel_id: any; listener_id: any; donation: any; comment: any}) => [
          livestreams.id, 
          livestreams.currentTime, 
          livestreams.date,
          livestreams.channel_id,
          livestreams.listener_id,
          livestreams.donation,
          livestreams.comment
        ]
      );
      setLivestreamData({ tableHead: ["ID", "Time", "Date", "channelID", "listenerID", "Donation", "Comment"], tableData });
      setLoading(false);
    })
    .catch((error) => {
      setError("error");
      setLoading(false);
    });
  }

  const get_youtubers = () => {
    // Fetch YouTubers data from API
    fetch("http://localhost:8000/api/subscriptions/youtubers") // Replace with your API endpoint
      .then((response) => response.json())
      .then((responseData) => {
        // Assuming responseData is an array of YouTubers with only name and id
        const tableData = responseData.map(
          (youtuber: { id: any; name: any }) => [
            youtuber.id, // Assuming 'id' is the unique identifier
            youtuber.name, // Assuming 'name' is the YouTuber's name
          ]
        );
        setYoutuberData({ tableHead: ["ID", "Name"], tableData });
        setLoading(false);
      })
      .catch((error) => {
        setError("error");
        setLoading(false);
      });
  }

  const toggle_button = (newView: React.SetStateAction<string>) => {
    setUserView(newView);
  };

  const render_customView = () => {
    return <Text style={styles.text}>{userView}</Text>;
  };

  return (
    <>
      <View style={styles.buttonContainer}>
        <Button
          title="Youtubers"
          onPress={() => toggle_button("youtubers")}
          color="green"
        />
        <Button
          title="Channels"
          onPress={() => toggle_button("channels")}
          color="green"
        />
        <Button
          title="LiveStreams"
          onPress={() => toggle_button("livestreams")}
          color="green"
        />
      </View>
      <View style={styles.container}>
        <Text style={styles.text}>Ranking</Text>
        {render_customView()}
      </View>
      <View style={styles.tableContainer}>
        {loading ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : error ? (
          <Text style={styles.text}>{error}</Text>
        ) : (userView==="livestreams") ? (
          <Table
          borderStyle={{ borderWidth: 4, borderColor: "teal" }}
          style={styles.table}
        >
          <Row
            data={livestreamdata.tableHead}
            style={styles.head}
            textStyle={styles.text}
          />
          <Rows data={livestreamdata.tableData} textStyle={styles.text} />
        </Table>
        )
        :(
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
