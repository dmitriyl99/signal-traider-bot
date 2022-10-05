import apiInstance from "./index";
import authApi from "./authApi";

function getUtmCommands() {
    return apiInstance.get('/utm/commands')
}

function saveUtmCommand(name) {
    return apiInstance.post('/utm/commands', {name})
}

function deleteUtmCommand(id) {
    return apiInstance.delete(`/utm/commands/${id}`);
}

function getUtmStatistics() {
    return apiInstance.get('/utm/commands/statistics');
}

export default {
    getUtmCommands, saveUtmCommand, deleteUtmCommand, getUtmStatistics
}