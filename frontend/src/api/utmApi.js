import apiInstance from "./index";

function getUtmCommands() {
    return apiInstance.get('/utm/commands')
}

function saveUtmCommand(name) {
    return apiInstance.post('/utm/commands', {name})
}

function deleteUtmCommand(id) {
    return apiInstance.delete(`/utm/commands/${id}`);
}

export default {
    getUtmCommands, saveUtmCommand, deleteUtmCommand
}