// Ocultar automáticamente el mensaje después de 5 segundos (5000 milisegundos)
setTimeout(function() {
var alertContainer = document.getElementsByClassName('alert-container')[0];
if (alertContainer) {
    alertContainer.style.display = 'none';
}
}, 5000);