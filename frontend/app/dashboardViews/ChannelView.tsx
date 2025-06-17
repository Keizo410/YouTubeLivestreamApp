import React from "react";
import { ScrollView } from "react-native";
import ChannelTableComponent from "@/components/channelTable";

export default function ChannelView({ data }: { data: any }) {
  return (
    <ScrollView>
      <ChannelTableComponent data={data} />
    </ScrollView>
  );
}
