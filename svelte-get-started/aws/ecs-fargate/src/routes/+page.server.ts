import { env } from "$env/dynamic/private";

export async function load() {
  const lfEnv = env.LAUNCHFLOW_ENVIRONMENT;
  return { props: { env: lfEnv } };
}
