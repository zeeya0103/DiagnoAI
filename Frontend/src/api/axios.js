import axios from "axios";

const api = axios.create({
  baseURL: "https://diagnoai-1-xywq.onrender.com",
});

export default api;