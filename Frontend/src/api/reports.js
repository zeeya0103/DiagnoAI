import api from "./axios";

// Upload Report
export const uploadReport = async (file) => {

  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post(
    "/reports/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

// Get Reports
export const getReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

// Delete Report
export const deleteReport = async (id) => {
  const response = await api.delete(`/reports/${id}`);
  return response.data;
};

// Download Report
export const downloadReport = async (id) => {
  const response = await api.get(`/reports/download/${id}`, {
    responseType: "blob",
  });

  return response.data;
};