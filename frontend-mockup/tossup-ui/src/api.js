
import axios from "axios";

const BASE_URL = "http://localhost:5000/api";

export const uploadVideo = async (file) => {
  const formData = new FormData();
  formData.append("video", file);
  const res = await axios.post(`${BASE_URL}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data;
};

export const analyzeVideo = async (upload_id) => {
  const res = await axios.post(`${BASE_URL}/analyze`, {
    upload_id,
    user_level: "intermediate",
    focus_areas: [],
    use_chatgpt: false
  });
  return res.data;
};
