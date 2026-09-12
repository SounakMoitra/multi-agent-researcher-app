import { useCallback, useEffect, useRef, useState } from "react";
import { getResearchJob } from "../api/client";

const ACTIVE_STATUSES = ["pending", "planning", "researching", "synthesizing"];
const POLL_INTERVAL_MS = 2000;

export function useResearchJob(jobId) {
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);
  const intervalRef = useRef(null);

  const fetchJob = useCallback(async () => {
    if (!jobId) return;
    try {
      const data = await getResearchJob(jobId);
      setJob(data);
      setError(null);
      if (!ACTIVE_STATUSES.includes(data.status) && intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
  }, [jobId]);

  useEffect(() => {
    if (!jobId) return undefined;

    setJob(null);
    setError(null);
    fetchJob();
    intervalRef.current = setInterval(fetchJob, POLL_INTERVAL_MS);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [jobId, fetchJob]);

  return { job, error };
}
