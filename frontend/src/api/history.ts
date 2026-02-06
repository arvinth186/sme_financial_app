import api from "./axios";

export const fetchHistory = async (industry: string) => {
  const res = await api.get(`/${industry.toLowerCase()}/analyses`);
  return res.data; // { count, results }
};
