import api from "./axios";

// AI Chat
export const askAI = async (message) => {

  const response = await api.post("/chatbot", {
    message,
  });

  return response.data;
};