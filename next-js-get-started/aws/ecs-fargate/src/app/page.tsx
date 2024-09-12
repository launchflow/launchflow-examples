import { unstable_noStore as noStore } from "next/cache";

export default function Home() {
  noStore();
  return <div>Hello from {process.env.LAUNCHFLOW_ENVIRONMENT}</div>;
}
