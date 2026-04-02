import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const generateVideo = async (data) => {
  const formData = new FormData();
  Object.keys(data).forEach(key => {
    formData.append(key, data[key]);
  });
  return axios.post(`${API_BASE_URL}/generate`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};