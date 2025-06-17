import React from "react";
import {
  View,
  ScrollView,
  TouchableOpacity,
  Text,
  useWindowDimensions,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import ChartComponent from "@/components/chart";
import BarComponent from "@/components/bar";
import LivestreamTableComponent from "@/components/LivestreamTable";

interface LivestreamData {
  chartData: any,
  barData: any,
  channelArray: any,
  screen: any,
  toggleScreen: any,
  styles: any
}
export default function LivestreamView({
  data
}: any) {
  return (
             <ScrollView>
              <LivestreamTableComponent data={data} />
              </ScrollView>
    // <View style={styles.chartBarContainer}>
    //   <SafeAreaView style={styles.chartBarChildContainer}>
    //     <ScrollView horizontal>
    //       {screen === "chart" ? (
    //         <ChartComponent chartData={chartData} channelArray={channelArray} />
    //       ) : (
    //         <BarComponent data={barData} />
    //       )}
    //     </ScrollView>
    //   </SafeAreaView>
    //   <View style={styles.chartBarButtonContainer}>
    //     <TouchableOpacity
    //       style={
    //         screen === "chart" ? styles.selectedButton : styles.button
    //       }
    //       onPress={() => toggleScreen("chart")}
    //     >
    //       <Text style={styles.buttonText}>Chart</Text>
    //     </TouchableOpacity>
    //     <TouchableOpacity
    //       style={
    //         screen === "livestream" ? styles.selectedButton : styles.button
    //       }
    //       onPress={() => toggleScreen("livestream")}
    //     >
    //       <Text style={styles.buttonText}>Bar</Text>
    //     </TouchableOpacity>
    //   </View>
    // </View>
  );
}
