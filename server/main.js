const socket = new WebSocket('ws://markmakave.com:8080');

socket.addEventListener('open', (event) => {
    console.log('Соединение установлено');
});

socket.addEventListener('message', (event) => {
    console.log(`Получено сообщение: ${event.data}`);
});