import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export async function startResearch(topic, modelName = "gpt-4o-mini") {
  const { data } = await client.post("/api/research", {
    topic,
    model_name: modelName,
  });
  return data;
}

export async function getResearchJob(jobId) {
  const { data } = await client.get(`/api/research/${jobId}`);
  return data;
}

export async function listResearchJobs() {
  const { data } = await client.get("/api/research");
  return data;
}

export async function deleteResearchJob(jobId) {
  const { data } = await client.delete(`/api/research/${jobId}`);
  return data;
}

export default client;
