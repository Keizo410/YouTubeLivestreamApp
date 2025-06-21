const BACKEND_URL = process.env.EXPO_PUBLIC_LOCAL_BACKEND_URL;

export async function fetchYoutubers() {
  console.log("here ", BACKEND_URL);
  const res = await fetch(`${BACKEND_URL}/api/subscriptions/youtubers`);
  if (!res.ok) {
    throw new Error("Youtuber fetching error");
  }

  const data = await res.json();

  console.log(res.status);

  return data.map((youtuber: { name: any }) => [youtuber.name]);
}

export async function fetchLivestreamsBarSummary() {
  const res = await fetch(`${BACKEND_URL}/api/livestreams/summary/bar`);
  if (!res.ok) {
    throw new Error("livestream summary(bar) fetching error");
  }

  const data = await res.json();

  return data;
}

export async function fetchLivestreamsChartSummary() {
  const res = await fetch(`${BACKEND_URL}/api/livestreams/summary/chart`);
  if (!res.ok) {
    throw new Error("livestream summary(chart) fetching error");
  }

  const data = await res.json();

  return data;
}

export async function fetchChannels() {
  const res = await fetch(`${BACKEND_URL}/api/subscriptions/channels`);
  if (!res.ok) {
    throw new Error("Channel fetching error");
  }

  const data = await res.json();
  // console.log(res.status);

  return data.map((channel: { name: any; youtuber: any; status: any }) => [
    channel.name,
    channel.youtuber,
    channel.status,
  ]);
}

export async function fetchLivestreams() {
  const res = await fetch(`${BACKEND_URL}/api/livestreams`);
  if (!res.ok) {
    throw new Error("Livestream fetching error");
  }

  const data = await res.json();

  return data.map(
    (livestreams: {
      currentTime: any;
      date: any;
      donation: any;
      comment: any;
    }) => [
      livestreams.currentTime,
      livestreams.date,
      livestreams.donation,
      livestreams.comment,
    ]
  );
}

export async function subscribeToYoutubers(youtuber: string) {
  const res = await fetch(`${BACKEND_URL}/api/subscriptions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ youtuber: youtuber }),
  });

  if (!res.ok) {
    throw new Error("Subscription error");
  }

  const data = await res.json();

  return [res, data];
}

export async function fetchChannelNum() {
  const res = await fetch(`${BACKEND_URL}/api/subscriptions/channels`);

  if (!res.ok) {
    throw new Error("Channel fetching error");
  }

  const data = await res.json();

  return data.length;
}

export async function fetchCurrentOnGoingLiveStream() {
  const res = await fetch(`${BACKEND_URL}/api/?`);

  if (!res.ok) {
    throw new Error("Current on-going livestream info fetching error!");
  }
  const data = await res.json();

  return data.map();
}

export async function fetchListeners() {
  const res = await fetch(`${BACKEND_URL}/api/channels/listeners`);

  console.log(res);

  if (!res.ok) {
    throw new Error("Listener Fetching Error!");
  }

  const data = await res.json();

  return data.map((listeners: { id: any; name: any; donation: any }) => [
    listeners.name,
    listeners.donation,
  ]);
}
