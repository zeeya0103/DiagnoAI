import api from "./axios";

// Book Appointment
export const bookAppointment = async (data) => {

  const response = await api.post(
    "/appointments",
    data
  );

  return response.data;
};

// Get Appointments
export const getAppointments = async () => {

  const response = await api.get(
    "/appointments"
  );

  return response.data;
};

// Cancel Appointment
export const cancelAppointment = async (id) => {

  const response = await api.delete(
    `/appointments/${id}`
  );

  return response.data;
};