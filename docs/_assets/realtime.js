// Real-time updates for dashboards
const socket = new WebSocket('ws://localhost:8080');

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Real-time update:', data);
    // Update the dashboard dynamically
};