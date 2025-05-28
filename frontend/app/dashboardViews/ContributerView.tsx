import React from "react";
import { ScrollView } from "react-native";
import ContributerTableComponent from "@/components/contributerTable";

export default function YoutuberView({ data }: { data: any }) {
  return (
    <ScrollView>
      <ContributerTableComponent data={data} />
    </ScrollView>
  );
}
