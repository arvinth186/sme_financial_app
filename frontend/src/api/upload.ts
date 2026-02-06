import api from "./axios";


const industryEndpointMap: Record<string, string> = {
  Agriculture: "agricultural",
  Manufacturing: "manufacturing",
  Retail: "retail",
  Logistics: "logistics",
  Ecommerce: "ecommerce",
};

export const uploadFinancialCSV = async (
  industry: string,
  file: File,
  language: string
) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", language);

  const endpoint = industryEndpointMap[industry];

  const response = await api.post(
    `/analyze/${endpoint}`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );

  return response.data;
};
