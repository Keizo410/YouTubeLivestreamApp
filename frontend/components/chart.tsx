import React from "react";
import { Dimensions, View } from "react-native";
import { CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis } from "recharts";

const { width, height } = Dimensions.get("window");
const lineColors = [
    "#8884d8", // purple
    "#82ca9d", // green
    "#ffc658", // yellow
    "#ff8042", // orange
    "#0088FE", // blue
    "#FF4069", // red
    "#00C49F", // teal
    "#FFBB28", // amber
    "#FF5733", // coral
    "#9467BD", // lavender
    "#8DD1E1", // light blue
    "#A4DE6C", // light green
  ];

interface ChartTypeProps {
    chartData: any,
    channelArray: string[]
}

export default function ChartComponent ({chartData, channelArray}:ChartTypeProps) {
  return (
    <View style={{width: "100%", height: "100%"}}>
      <LineChart width={width} height={0.6 * height} data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        {channelArray.map((channel, index) => (
          <Line
            key={channel}
            type="monotone"
            dataKey={channel as string}
            stroke={lineColors[index % lineColors.length]}
          />
        ))}
      </LineChart>
    </View>
  );
};

