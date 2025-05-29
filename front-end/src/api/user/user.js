import api from '../api';

export const userLogin = async (user) => {return await api.post('/users/login', user);};
export const validateToken = async (token) => {  return await api.post('/users/validateToken', {token});};