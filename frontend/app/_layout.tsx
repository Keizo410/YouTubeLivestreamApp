import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen name="+not-found" />
      <Stack.Screen name="success" options={{headerShown: false}}/>
      <Stack.Screen name="failedSubscription" options={{headerShown: false}}/>
    </Stack>
  );
}
