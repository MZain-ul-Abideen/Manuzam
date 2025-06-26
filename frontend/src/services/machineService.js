import api from '../api';

export async function getMachines() {
  const response = await api.get('/machines/');
  return response.data;
}

export async function getMachineById(machineId) {
  const response = await api.get(`/machines/${machineId}`);
  return response.data;
}

export async function createMachine(machineData) {
  const response = await api.post('/machines/', machineData)
  return response.data
}

export async function updateMachine(machineId, machineData) {
  const response = await api.put(`/machines/${machineId}`, machineData);
  return response.data;
}

export async function deleteMachine(machineId) {
  const response = await api.delete(`/machines/${machineId}`);
  return response.data;
}
