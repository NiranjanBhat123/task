import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginUser = async (username, password) => {
  const response = await api.post('/token/', { username, password });
  return response.data;
};

export const registerUser = async (username, email, password) => {
  const response = await api.post('/register/', { username, email, password });
  return response.data;
};

export const getProjects = async () => {
  const response = await api.get('/projects/');
  console.log(response.data);
  return response.data;
};

export const getProject = async (id) => {
  const response = await api.get(`/projects/${id}/`);
  console.log(response.data);
  return response.data;
};

export const createProject = async (projectData) => {
  const response = await api.post('/projects/', projectData);
  console.log(response.data);
  return response.data;
};


export const getUsers = async () => {
  const response = await api.get('/users/');
  return response.data;
};


