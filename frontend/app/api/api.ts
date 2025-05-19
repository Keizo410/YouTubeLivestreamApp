const BACKEND_URL = process.env.EXPO_PUBLIC_PROD_BACKEND_URL;

export async function fetchYoutubers() {
  const res = await fetch(`${BACKEND_URL}/api/subscriptions/youtubers`);
  if (!res.ok) {
    throw new Error("Youtuber fetching error");
  }

  const data = await res.json();

  console.log(res.status);

  return data.map((youtuber: { id: any; name: any }) => [
    youtuber.id,
    youtuber.name,
  ]);
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
  console.log(res.status);

  return data.map((channel: { id: any; name: any; youtuber: any }) => [
    channel.id,
    channel.name,
    channel.youtuber,
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
      id: any;
      currentTime: any;
      date: any;
      channel_id: any;
      listener_id: any;
      donation: any;
      comment: any;
    }) => [
      livestreams.id,
      livestreams.currentTime,
      livestreams.date,
      livestreams.channel_id,
      livestreams.listener_id,
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
