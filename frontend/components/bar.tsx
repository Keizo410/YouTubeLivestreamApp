import React from "react";
import { Dimensions, ScrollView, View } from "react-native";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const { width, height } = Dimensions.get("window");

interface BarTypeProps {
  data: any;
}

export default function BarComponent({ data }: BarTypeProps) {
  return (
    <View style={{ width: "100%", height: "100%" }}>
      <BarChart
        width={Math.max(data.length * 100, width)}
        height={height * 0.6}
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
        barSize={20}
      >
        <XAxis dataKey="name" scale="point" padding={{ left: 10, right: 10 }} />
        <YAxis />
        <Tooltip />
        <Legend />
        <CartesianGrid strokeDasharray="3 3" />
        <Bar dataKey="sales" fill="#8884d8" background={{ fill: "#eee" }} />
      </BarChart>
    </View>
  );
}
