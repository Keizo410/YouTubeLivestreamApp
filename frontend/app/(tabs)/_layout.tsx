import { Tabs } from "expo-router";
import Ionicons from "@expo/vector-icons/Ionicons";
import FontAwesome6 from "@expo/vector-icons/FontAwesome6";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#5fa8d3",
        // tabBarActiveTintColor: "#ffd33d",
        headerStyle: {
          // backgroundColor: "#25292e",
        },
        headerShadowVisible: false,
        // headerTintColor: "#fff",
        tabBarStyle: {
          // backgroundColor: "#25292e",
        },
        tabBarLabelStyle: {
          fontSize: 15,  // Adjust the size as needed
          fontWeight: "bold", 
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={focused ? "home-sharp" : "home-outline"}
              color={color}
              size={25}
            />
            
          ),
        }}
      />
      <Tabs.Screen
        name="about"
        options={{
          title: "About",
          tabBarIcon: ({ color, focused }) => (
            <Ionicons
              name={
                focused ? "information-circle" : "information-circle-outline"
              }
              color={color}
              size={25}
            />
          ),
        }}
      />
      <Tabs.Screen
        name="ranking"
        options={{
          title: "Ranking",
          tabBarIcon: ({ color, focused }) => (
            <FontAwesome6 name="ranking-star" size={25} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
