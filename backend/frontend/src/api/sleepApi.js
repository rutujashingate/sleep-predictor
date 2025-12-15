import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const predictSurveySleep = async (data) => {
  const res = await axios.post(`${API_BASE}/predict_survey`, data);
  return res.data;
};

export const predictSmartwatchSleep = async (data) => {
  const res = await axios.post(`${API_BASE}/predict_smartwatch`, data);
  return res.data;
};
